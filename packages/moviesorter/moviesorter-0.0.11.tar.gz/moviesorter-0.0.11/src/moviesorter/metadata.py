import asyncio
import logging
import random
import re
from enum import Enum
from typing import Dict, Optional, Tuple, Callable, Any
from urllib.parse import quote

import aiohttp
from aiohttp import ClientResponseError
from cache import AsyncLRU
from pydantic import BaseModel

from .config import MetadataProviderApi

log = logging.getLogger(".".join([__package__, __name__]))


class MetadataQueryError(Exception):
    pass


class MetadataNotFoundError(MetadataQueryError):

    search_term: str


class TvShowMetadata(BaseModel):
    series_title: str
    season_id: int
    episode_title: str
    episode_id: int


class MovieMetadata(BaseModel):
    title: str
    year: int


class MetadataApi:

    # These attributes can be hard-coded in the implementation
    # and overriden via configuration.
    key: str = None
    url: str = None
    path: str = None
    configured_overrides: Dict[str, str]

    def __init__(
        self, config: MetadataProviderApi = None, search_overrides: Dict[str, str] = None
    ) -> None:
        if config and config.key:
            self.key = config.key
        if config and config.url:
            self.url = config.url
        if config and config.path:
            self.path = config.path
        self.configured_overrides = search_overrides or {}

    async def query(self, *args, **kwargs):
        """
        The high level query function used to query the database. Returns media metadata
        in a format specific to the actual implementation.

        MUST return a valid response, otherwise raise any MetadataQueryException.
        """
        raise NotImplemented

    @staticmethod
    @AsyncLRU(maxsize=1024)
    async def request(url: str) -> dict:
        """
        A wrapper around the actual request that caches a successful response is obtained.
        Otherwise, ClientResponseError is raised.

        :param url: Specify the url that we want to request
        :return: A json object
        """
        log.debug(f"Network request: [GET]({url})")
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()  # Raised errors don't get cached.
                data = await response.json()
        return data

    async def async_fetch_json(self, url, retry=0, max_retries=4):
        """
        A wrapper around the requests function that handles retries and error handling.
        It returns the raw JSON response, or raises an exception if it eventually fails
        to get a valid response.

        :param url: specify the url to fetch
        :param retry: int: retry counter (0 = the actual 1st request, not a re-try yet)
        :param max_retries: int: limit the number of retries in case of a 429 or 503 errors
        :return: the result of the metadata API
        """
        log.debug(f"fetching '{url}', retries={retry}/{max_retries}")
        try:
            return await MetadataApi.request(url)
        except ClientResponseError as e:
            # Running too many queries at once causes the API (TV Maze at the very least)
            # to decline our requests. Simple wait and retry seems to be sufficient.
            if e.status in (429, 503) and retry < max_retries:
                wait_sec = random.randint(10, 100) / 100 * (retry + 1)
                log.warning(f"Service unavailable, retrying in {wait_sec}s.")
                await asyncio.sleep(wait_sec)
                return await self.async_fetch_json(url, retry + 1)
            raise MetadataQueryError(e)

    async def try_harder(
            self,
            search_term: str,
            validation_callback: Callable[[dict, Any], Any] = None,  # must raise
            validation_callback_args: Tuple = None,
            to_be_raised: Exception = None,
            try_index: int = 1,
            min_len: int = 1
    ) -> dict:
        """
        A helper function that tries to find the metadata by searching for it in an iterative way.
        It does this by removing one word from the end of the search term and trying again. If it
        fails, then it removes another word and tries again until min_len is reached.

        :param search_term: Search for the show
        :param validation_callback: Validate the response data (! must raise MetadataQueryException)
        :param validation_callback_args:Tuple=None: Pass arguments to the validation callback
        :param to_be_raised: Pass an exception to be raised once the function eventually fails.
        :param try_index: Keep track of the number of tries
        :param min_len: set the minimum words count to be searched for.
        :return: The response data "as-is" if it matches provided validation fn.
        """
        split = search_term.split()

        while len(split) >= min_len:
            search_title = quote(self.clean_search_term(" ".join(split)))
            log.info(f"{try_index}. try: search='{search_title}'")
            show_url = self.url + "/" + self.path.format(title=search_title)
            try:
                response_data = await self.async_fetch_json(show_url)
                await validation_callback(response_data, *(validation_callback_args or tuple()))
                return response_data
            except MetadataQueryError as e:
                if not to_be_raised:
                    to_be_raised = e
                return await self.try_harder(
                    search_term=" ".join(split[:-1]),
                    validation_callback=validation_callback,
                    validation_callback_args=validation_callback_args,
                    to_be_raised=to_be_raised,  # propagate "the original" exc
                    try_index=try_index + 1,
                    min_len=min_len
                )
        raise to_be_raised or MetadataQueryError(f"No exception provided, query failed: "
                                                 f"{search_term=}, {try_index}. try.")

    def clean_search_term(self, string):
        parts = string.split()
        if not parts:
            parts = [string]

        # Skip all the words "the" in the title, because TVMaze seems to choke on this.
        # * The leading 'the' needs to be preserved though...
        first_the = None
        if re.match('^[Tt]he$', parts[0]):
            first_the = parts.pop(0)
        parts = [word for word in parts if not re.match('^[Tt]he$', word)]
        if first_the:
            parts.insert(0, first_the)

        # rejoin
        # search_title = ' '.join(parts)  # This seems to yield better results than '+'.
        search_title = ' '.join(parts)  # This seems to yield better results than '+'.

        # search_title = title
        if search_title in self.configured_overrides:
            new_name = self.configured_overrides[string]
            log.debug(f"Overriding search title: '{string}' -> '{new_name}'")
            search_title = new_name

        search_title = search_title.replace("'", "")

        return search_title


class TvShowMetadataApi(MetadataApi):

    async def query(self, title: str, season_id: int, episode_id: int) -> TvShowMetadata:
        raise NotImplemented


class MovieMetadataApi(MetadataApi):

    async def query(self, title: str, year: str) -> MovieMetadata:
        raise NotImplemented


class TvMaze(TvShowMetadataApi):

    # Base URL for TV Maze; should generally not be changed (can be overriden via config)
    url: str = "https://api.tvmaze.com"

    # Search path for TV Maze; should generally not be changed (can be overriden via config)
    # Variables replaced at runtime:
    #  * "title": the show name query, extracted from the source filename
    path = "singlesearch/shows?q={title}&embed=episodes"

    async def _match_tv_show(self, series_data: dict, season_id: int, episode_id: int) -> dict:
        """
        Find the correct episode in the series episodes list.

        :param series_data: dict: Pass the data from _get_series_data() to _match_tv_show()
        :param season_id: int: Specify the season number
        :param episode_id: int: Specify the episode number
        :return: A dictionary with the episode data
        """

        def find_episode(e_list):
            for episode in e_list:
                if episode.get('season') == season_id and episode.get('number') == episode_id:
                    return episode

        episode_list = series_data['_embedded'].get('episodes', [])
        correct_episode = find_episode(episode_list)
        if not correct_episode:
            log.warning(f"Episode {season_id=} {episode_id=} not found.")

            if series_data.get("_links") and series_data["_links"].get("self"):
                alternative_url = series_data["_links"]["self"]["href"] + "/episodes?specials=True"
                log.debug(f"Trying alternative URL: {alternative_url}")

                episode_list = await self.async_fetch_json(alternative_url)

                correct_episode = find_episode(episode_list)
                if not correct_episode:
                    # One last try - maybe TV Maze does not show the episode id,
                    # e.g. a special episode (?)
                    season_only = list(filter(lambda e: e["season"] == season_id, episode_list))
                    season_only.sort(key=lambda e: e["airdate"])
                    log.info(f"{len(season_only)} {episode_id=}")
                    episode_list = season_only
                    if len(season_only) >= episode_id:
                        # Yay! We should have a match. Just grab the episode by index
                        # (assuming the 'air date' ordering is valid).
                        correct_episode = season_only[episode_id - 1]

        if not correct_episode:
            episodes = [f"S{e.get('season')}E{e.get('number')}" for e in episode_list]
            msg = f"TV show {series_data.get('name')} found, BUT correct " \
                  f"episode {season_id=}, {episode_id=} can't be found in {episodes}"
            raise MetadataQueryError(msg)
        return correct_episode

    async def query(self, title: str, season_id: int, episode_id: int) -> TvShowMetadata:

        series_data = await self.try_harder(
            search_term=title,
            validation_callback=self._match_tv_show,
            validation_callback_args=(season_id, episode_id)
        )
        log.debug(f"Found metadata for series '{series_data.get('name')}'")
        # Get the series and episode titles
        series_title = series_data.get('name')
        episode_title = (
            await self._match_tv_show(series_data, season_id, episode_id)
        ).get('name', 'Unnamed')

        # Sometimes, we get a slash; only invalid char on *NIX so replace it
        episode_title = episode_title.replace('/', '-')

        return TvShowMetadata(
            series_title=series_title,
            season_id=season_id,
            episode_title=episode_title,
            episode_id=episode_id
        )


class TMDB(MovieMetadataApi):

    # Base URL for TMDB; should generally not be changed (can be overriden via config)
    url: str = "https://api.themoviedb.org/3"

    # Search path for TMDB; should generally not be changed (can be overriden via config)
    # Variables replaced at runtime:
    #  * "key": the TMDB API key specified above
    #  * "title": the movie name query, extracted from the source filename
    path: str = "search/movie?api_key={key}&query={title}"

    def __init__(
            self, config: MetadataProviderApi = None, search_overrides: Dict[str, str] = None
    ) -> None:
        super().__init__(config, search_overrides)
        self.path = self.path.format(key=self.key, title='{title}')

    def clean_search_term(self, string):
        # "Sanitize" input name...

        # Remove the first "The" from the title when searching to avoid weird conflicts
        search_movie_title = re.sub("[Tt]he\+", "", string, 1)
        # Apply overrides
        if search_movie_title in self.configured_overrides:
            new_name = self.configured_overrides[search_movie_title]
            log.debug(f"Overriding search title: '{search_movie_title}' -> '{new_name}'")
            search_movie_title = new_name

        return search_movie_title

    @staticmethod
    async def _match_movie(movie_data: dict, search_year: int = None):
        # List all movies and find the one matching the year (within year on either side)
        result_list = movie_data.get('results')

        if not result_list:
            raise MetadataQueryError("Results list is empty.")

        result_movie_title = None
        result_movie_year = None
        for movie in result_list:
            try:
                release_year = int(movie.get('release_date', '0000-00-00').split('-')[0])
            except (TypeError, ValueError):
                release_year = 0  # No release year.

            if not search_year or search_year == release_year:
                result_movie_title = movie.get('title')
                result_movie_year = release_year
                break
            elif abs(release_year - search_year) == 1:
                result_movie_title = movie.get('title')
                result_movie_year = release_year
                # Candidate, but don't break

        if not result_movie_title:
            raise MetadataQueryError(
                f"Movie search produced results, BUT the requested {search_year=} not found in: "
                f"{['{title}/{release_date}'.format(**mov) for mov in result_list]}"
            )

        return result_movie_title, result_movie_year

    async def query(self, search_movie_title: str, search_year: int) -> Optional[MovieMetadata]:
        if not self.key:
            raise MetadataQueryError(f"{self.__class__.__name__}: key required.")

        movie_data = await self.try_harder(
            search_term=search_movie_title,
            validation_callback=self._match_movie,
            validation_callback_args=(search_year,)
        )

        if not movie_data or not movie_data.get('results'):
            raise MetadataQueryError(
                f"Movie query for '{search_movie_title}' {search_year=} produced no results."
            )
        result_movie_title, result_movie_year = await self._match_movie(movie_data, search_year)

        return MovieMetadata(title=result_movie_title, year=result_movie_year)


class MetadataProvider(Enum):
    """List of all available (implemented) metadata providers."""
    TV_MAZE = "tvmaze"
    TMDB = "tmdb"

    @property
    def clazz(self):
        return {
            MetadataProvider.TV_MAZE.value: TvMaze,
            MetadataProvider.TMDB.value: TMDB,
        }.get(self.value)
