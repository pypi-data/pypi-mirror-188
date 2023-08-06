"""
moviesorter.py - Sort a media file into an organized library

Copyright (C) 2020  Joshua M. Boniface <joshua@boniface.me>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import asyncio
import logging
import os
import re
import subprocess
from subprocess import DEVNULL
from enum import Enum
from pathlib import Path
from typing import Optional, List, Union

from functools import lru_cache

try:
    # missing on Windows
    import grp
except (ImportError, ModuleNotFoundError):
    grp = None

try:
    # missing on Windows
    import pwd
except (ImportError, ModuleNotFoundError):
    pwd = None

from pydantic import BaseModel

from .config import Config, ScanConfig, MetadataProviderApi
from .metadata import (
    TvShowMetadata,
    MovieMetadata,
    MetadataApi,
    TvShowMetadataApi,
    MovieMetadataApi,
    MetadataQueryError,
    MetadataProvider,
)
from .parser import (
    parse_season_and_episode,
    parse_movie_name,
    fix_leading_the,
    split_basename,
    ParsingError
)


log = logging.getLogger(".".join([__package__, __name__]))


class Action(Enum):
    MOVE = "move"
    HARDLINK = "hardlink"
    SYMLINK = "symlink"
    COPY = "copy"


class MediaType(Enum):
    TV_SHOW = "tv"
    MOVIE = "movie"
    AUTO = "auto"


class State(str, Enum):
    OK = "ok"
    SUCCESS = "success"
    ERROR = "error"


class Operation(BaseModel):
    input_path: str
    output_path: Optional[str]
    state: State = State.OK
    action: Action = Action.COPY
    type: Optional[MediaType]
    log: List[str] = []

    def error(self, msg=None):
        self.state = State.ERROR
        if msg:
            self.log.append(f"ERROR: {msg}")
        return self

    @property
    def is_error(self):
        return self.state == State.ERROR


class MediaSorterException(Exception):
    pass


class MediaSorter:

    config: Config
    source_path: str
    restrict_media_type: MediaType = MediaType.AUTO
    allow_metainfo_tagging: bool = False
    tv_show_destination: Optional[str]
    movies_destination: Optional[str]

    def __init__(
            self,
            config,
            source_path=None,
            restrict_media_type: MediaType = MediaType.AUTO,
            tv_show_destination=None,
            movies_destination=None,
            allow_metainfo_tagging=False
    ) -> None:
        self.config = config
        self.source_path = source_path
        self.restrict_media_type = restrict_media_type
        self.tv_show_destination = tv_show_destination
        self.movies_destination = movies_destination
        self.allow_metainfo_tagging = allow_metainfo_tagging

    async def scan(self, src_path: str = None) -> List[Operation]:
        operations = []

        src_path = src_path if src_path else self.source_path
        if os.path.isdir(src_path):
            tasks = []
            log.debug(f"Scanning {src_path} [{self.restrict_media_type}]")
            for filename in sorted(os.listdir(src_path)):
                child_path = os.path.join(src_path, filename)
                tasks.append(asyncio.ensure_future(self.scan(child_path)))

            results = await asyncio.gather(*tasks)
            for res in results:
                operations.extend(res)
        elif not os.path.exists(src_path):
            log.error(f"{src_path}: path does not exist!")
            op = Operation(input_path=src_path, state=State.ERROR)
            op.error("Path does not exist")
            operations.append(op)
        else:
            operations.append(
                await self.suggest(src_path, media_type=self.restrict_media_type)
            )

        return [op for op in operations if op]

    def _get_api(self, api: MetadataProviderApi) -> Optional[MetadataApi]:
        """API instantiation and null check for the Enum(<str>)."""
        try:
            return MetadataProvider(api.name).clazz(api, self.config.search_overrides)
        except ValueError:
            log.warning(
                f"'{api.name}' API provider "
                f"not recognized among {[e.value for e in MetadataProvider]}"
            )

    def _get_apis(self, type_: type[MetadataApi]) -> List[MetadataApi]:
        """Get all available MD providers by type."""
        return list(
            filter(
                lambda x: x is not None, filter(
                    lambda provider: isinstance(provider, type_), map(
                        lambda api: self._get_api(api), self.config.apis)
                )
            )
        )

    async def _query(
        self, api_type: type[MetadataApi], *args
    ) -> Union[TvShowMetadata, MovieMetadata]:
        """Make an external query to find a TV-show/movie metadata."""
        apis = self._get_apis(api_type)
        if not apis:
            msg = f"No '{api_type.__name__}' metadata provider APIs configured."
            log.error(msg)
            raise MediaSorterException(msg)

        # Try to fetch info from all available APIs at once, return only the first result
        api_queries = [asyncio.create_task(api.query(*args)) for api in apis]
        exceptions = []
        for api_query in asyncio.as_completed(api_queries):
            try:
                first_result = await api_query
            except MetadataQueryError as e:
                log.warning(str(e))
                exceptions.append(e)
                continue
            if first_result:
                return first_result

        exceptions.append(
            MediaSorterException(
                f"{api_type.__name__}: none of the "
                f"{[a.__class__.__name__ for a in apis]} APIs was successful"
            )
        )
        raise MediaSorterException(exceptions)

    async def suggest_tv_show(self, src_path: str):
        parsed_tv_show = parse_season_and_episode(
            src_path,
            self.config.split_characters,
            self.config.min_split_length,
            force=True  # Try everything!
        )

        if parsed_tv_show:
            if not self.tv_show_destination:
                raise MediaSorterException("TV shows destination dir not specified.")
            name, series, episode = parsed_tv_show

            log.debug(f"TV show recognized: series='{name}' S={series} E={episode}")
            result = await self._query(TvShowMetadataApi, name, series, episode)

            if self.config.suffix_the:
                result.series_title = fix_leading_the(result.series_title)

            # Build the final path+filename
            season_dir = self.config.tv_show_dir_format.format(**result.__dict__)
            filename = self.config.tv_show_format.format(**result.__dict__)

            # Custom join character for multi-word names (instead of " ")
            filename = self.config.join_character.join(filename.split())

            return season_dir, filename

    async def suggest_movie(self, src_path: str) -> str:
        """
        Suggest the title of the movie, as well as its year based on an external metadata
        API query. If it cannot find any results, it will return None for both title and year.

        :param src_path: str: Specify the path to the file that is going to be moved
        :return: A final, formatted movie file name suggestion
        :rtype: str
        """

        if not self.movies_destination:
            raise MediaSorterException("Movies destination dir not specified.")

        # Even if movie type is forced, try to find the season/episode numbers
        # to disqualify the media file before any network requests.
        try:
            if parse_season_and_episode(
                    src_path,
                    self.config.split_characters,
                    self.config.min_split_length,
                    force=False  # We DON'T want to parse a TV show at all costs.
            ):
                raise MediaSorterException(f"This appears to be a TV show: {src_path}")
        except ParsingError:
            pass

        movie, year = parse_movie_name(
            src_path, self.config.split_characters, self.config.min_split_length
        )
        result = await self._query(MovieMetadataApi, movie, year)

        for title in self.config.movie_name_overrides:
            if title == result.title:
                result.title = self.config.movie_name_overrides[title]
                break

        metainfo = list()
        if self.allow_metainfo_tagging:
            # Pull metainfo from filename if it is in the map
            basename_parts = split_basename(
                src_path, self.config.split_characters, self.config.min_split_length
            )
            for item in self.config.metainfo_map:
                for idx, element in enumerate(basename_parts):
                    key, value = list(item.items())[0]
                    if re.fullmatch(key, element) and value not in metainfo:
                        metainfo.append(value)

        # Custom join character for multi-word names.
        result.title = self.config.join_character.join(result.title.split())

        filename = self.config.movie_format.format(**result.__dict__)
        if metainfo:
            filename = self.config.join_character.join([filename, f"[{' '.join(metainfo)}]"])

        return filename.strip()

    async def suggest(
            self, src_path: str, media_type: MediaType = MediaType.AUTO
    ) -> Optional[Operation]:
        operation = Operation(input_path=src_path)
        extension = os.path.splitext(src_path)[-1]

        log.info(f">>> Parsing {src_path} [{media_type}]")

        if not extension:
            log.warning(f"{os.path.basename(src_path)}: file without an extension not allowed.")
            return None
        elif extension and extension not in self.config.valid_extensions:
            log.warning(
                f"{os.path.basename(src_path)}: extension '{extension}' not allowed, "
                f"not in {self.config.valid_extensions}."
            )
            return None

        # First try to parse a TV show (series and episodes numbers)
        operation.type = MediaType.TV_SHOW
        if media_type in [MediaType.AUTO, MediaType.TV_SHOW]:
            try:
                season_dir, filename = await self.suggest_tv_show(src_path)
                filename += extension

                # Build the final path+filename
                suggested_dest = os.path.join(self.tv_show_destination, season_dir, filename)
                operation.output_path = suggested_dest
                log.debug(f"Suggested output path: {suggested_dest}")

                return operation
            except TypeError as e:
                x = 15
                raise
                pass  # season_dir, filename = None
            except ParsingError as e:
                msg = f"{os.path.basename(src_path)} can't be parsed into a TV show: {e}."
                if media_type == MediaType.TV_SHOW:
                    log.error(msg)
                    return operation.error(msg)
                log.debug(msg)
                operation.log.append(msg)
            except (MediaSorterException, MetadataQueryError) as e:
                return operation.error(msg=str(e))

        # Not a TV show? Must be a movie then...
        operation.type = MediaType.MOVIE
        try:
            filename = await self.suggest_movie(src_path)
        except (MediaSorterException, ParsingError) as e:
            msg = f"{os.path.basename(src_path)} can't be parsed into a movie title: {e}."
            log.error(msg)
            return operation.error(msg)
        except (MediaSorterException, MetadataQueryError) as e:
            return operation.error(msg=str(e))

        # Build the final path+filename
        dst_path = os.path.join(self.movies_destination, filename)
        dst_path += extension
        log.debug(f"Suggested output path: {dst_path}")
        operation.output_path = dst_path

        return operation

    @staticmethod
    async def commit_all(
            operations: List[Operation],
            user: str = None,
            group: str = None,
            chown: bool = False,
            dir_mode: str = None,
            file_mode: str = None,
            overwrite: bool = False,
            infofile: bool = False,
            shasum: bool = False
    ) -> List[Operation]:
        tasks = []
        for sort_operation in operations:
            tasks.append(
                MediaSorter.commit(
                    sort_operation,
                    user=user,
                    group=group,
                    chown=chown,
                    infofile=infofile,
                    shasum=shasum,
                    file_mode=file_mode,
                    overwrite=overwrite,
                    dir_mode=dir_mode
                )
            )
        return await asyncio.gather(*tasks)

    @staticmethod
    async def commit(
            operation: Operation,
            user: str = None,
            group: str = None,
            chown: bool = False,
            dir_mode: str = None,
            file_mode: str = None,
            overwrite: bool = False,
            infofile: bool = False,
            shasum: bool = False
    ) -> Operation:
        # Change target file ownership

        if chown and user:
            if not pwd:
                return operation.error(f"'pwd' module not found, can't use --chown.")
            uid = pwd.getpwnam(user)[2]
        else:
            uid = os.getuid()

        if chown and group:
            if not grp:
                return operation.error(f"'grp' module not found, can't use --chown.")
            gid = grp.getgrnam(group)[2]
        else:
            gid = os.getgid()

        if not operation.output_path:
            return operation.error(f"{operation} does not proved a valid destination path.")

        if operation.action == Action.SYMLINK:
            action_cmd = ['ln', '-s', f"{operation.input_path}", f"{operation.output_path}"]
        elif operation.action == Action.HARDLINK:
            action_cmd = ['ln', f"{operation.input_path}", f"{operation.output_path}"]
        elif operation.action == Action.COPY:
            action_cmd = ['cp', f"{operation.input_path}", f"{operation.output_path}"]
        elif operation.action == Action.MOVE:
            action_cmd = ['mv', f"{operation.input_path}", f"{operation.output_path}"]
        else:
            return operation.error(f"Unexpected action option: '{operation.action}'")

        # Ensure our dst_path exists or create it.
        parent_dir = os.path.dirname(operation.output_path)
        if not os.path.isdir(parent_dir):
            log.info(f"Creating target directory '{parent_dir}'")
            os.makedirs(parent_dir)
            if chown:
                os.chown(parent_dir, uid, gid)
                if dir_mode:
                    os.chmod(parent_dir, int(dir_mode, 8))

        # Handle overwrite by removing existing dest file.
        dst_path = Path(operation.output_path)
        if dst_path.exists():
            log.info(f"File exists '{operation.output_path}'")
            if overwrite:
                log.info(f"Removing for overwrite.")
                os.remove(operation.output_path)
            else:
                msg = f"Destination file '{operation.output_path}' exists; skipping."
                log.error(msg)
                return operation.error(msg)

        # Run the action.
        log.info(f"Running sort action: {action_cmd}")
        process = subprocess.run(action_cmd, stdout=DEVNULL, stderr=DEVNULL)
        retcode = process.returncode

        if retcode != 0:
            log.error(f"Sort action '{action_cmd}' failed. {process.stdout=}, {process.stderr=}")
            return operation \
                .error(f"Sort action '{action_cmd}' failed.") \
                .error(f"STDOUT: {process.stdout}") \
                .error(f"STDERR: {process.stderr}")

        if chown:
            log.info(f"Correcting ownership and permissions: {uid=}, {gid=}, {file_mode=}")
            os.chown(operation.output_path, uid, gid)
            os.chmod(operation.output_path, int(file_mode, 8))

        # Create the info file.
        if infofile:
            info_file_name = f"{operation.output_path}.txt"
            log.info(f"Creating info file: .../{os.path.basename(info_file_name)}")
            info_file_contents = [
                "Source filename:  {}".format(os.path.basename(operation.output_path)),
                "Source directory: {}".format(os.path.dirname(operation.output_path))
            ]
            with open(info_file_name, 'w') as fh:
                fh.write('\n'.join(info_file_contents))
                fh.write('\n')
            if chown:
                os.chown(info_file_name, uid, gid)
                os.chmod(info_file_name, int(file_mode, 8))

        # Create sha256sum file
        if shasum:
            shasum_name = '{}.sha256sum'.format(operation.output_path)
            log.debug(f"Generating shasum file: .../'{os.path.basename(shasum_name)}'.")
            shasum_cmdout = subprocess.run(
                ['sha256sum', '-b', f'{operation.output_path}'],
                capture_output=True, encoding='utf8'
            )
            if shasum_cmdout.returncode != 0 or not shasum_cmdout.stdout:
                return operation \
                    .error("SHASUM checksum generation failed.") \
                    .error(f"STDOUT: {shasum_cmdout.stdout}") \
                    .error(f"STDERR: {shasum_cmdout.stderr}")

            shasum_data = shasum_cmdout.stdout.strip()
            log.info(f".../{os.path.basename(operation.output_path)}: SHA generated {shasum_data}.")
            with open(shasum_name, 'w') as fh:
                fh.write(shasum_data)
                fh.write('\n')
            if chown:
                log.debug(f"{os.path.basename(shasum_name)}: changing owner.")
                os.chown(shasum_name, uid, gid)
                os.chmod(shasum_name, int(file_mode, 8))

        operation.state = State.SUCCESS
        return operation

