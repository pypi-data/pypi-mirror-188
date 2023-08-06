###############################################################################
# CLICK
##############################################################################
import asyncio
import logging
import os
import sys
from typing import Tuple, List

import click
from rich.console import Console
from rich.prompt import Confirm
from rich.text import Text

from moviesorter.config import Config, read_config
from moviesorter.sorter import MediaSorter, Action, State, MediaType, Operation

FORMAT = "%(asctime)s [%(levelname)s] %(message)s"
logging.basicConfig(level="NOTSET", format=FORMAT)
logging.getLogger('asyncio').setLevel(logging.WARNING)

log = logging.getLogger()

# Global Click options
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'], max_content_width=120)


def _pretty_print_operation(sort_operation, console, before=False, verbose=False):
    if before and sort_operation.state in State.OK:
        console.print(Text(f"○ {sort_operation.input_path}", style="green"))
        console.print(Text(f"   ⤷  [{sort_operation.action.value}] {sort_operation.output_path}", style="green"))
    elif sort_operation.state in State.SUCCESS:
        console.print(Text(f" ✓ {sort_operation.output_path}", style="green"))

    elif sort_operation.state == State.ERROR:
        console.print(Text(f"○ {sort_operation.input_path}", style="red"))
        for line in sort_operation.log:
            if 'ERROR' in line:
                console.print(Text(f"   ⤬ {line.replace('ERROR: ', '')}", style="#fe9797"))
            elif verbose:
                console.print(Text(f"   ▸ {line}", style="gray"))
    else:
        console.print(Text(f"⚠ {sort_operation.input_path}", style="yellow bold"))
        for line in sort_operation.log:
            console.print(Text(f"   ⚠ {line}"))


def _load_config(console, config_file, verbose=False) -> Config:
    # Load configuration file.
    msgs = []
    try:
        return read_config(config_file)
    except FileNotFoundError:
        msgs.append(
            Text(f"Can't load configuration '{config_file}', file not found", style="yellow")
        )
    except KeyError as e:
        msgs.append(
            Text(
                f"Can't load configuration '{config_file}', invalid config keys.",
                style="yellow"
            )
        )
        if verbose:
            log.exception(e)
    except Exception as e:
        msgs.append(
            Text(
                f"Can't load configuration from '{config_file}', unexpected error {e} ",
                style="yellow"
            )
        )
        if verbose:
            log.exception(e)

    for msg in msgs:
        console.print(msg)
    console.print(Text(f"Hard-coded defaults assumed (!)"))
    return Config()


@click.command(
    context_settings=CONTEXT_SETTINGS,
    help="Scan and sort one or more source files/directories (directories will be crawled"
         "recursively). Media sources (and respective destination paths) can also be specified "
         "using the configuration file.\n\n"
         "Metadata will be searched for using configured APIs and media file names"
         "will be renamed accordingly."
)
@click.option(
    '-d', '--destination', 'dst_path',
    type=click.Path(),
    default='~/Media', show_default=True,
    help='The target directory to sort to'
)
@click.option(
    '-dtv', '--destination-tv', 'dst_path_tv',
    type=click.Path(),
    default='~/Media', show_default=True,
    help='The target directory to sort to: TV shows ONLY, shadows the --destination option'
)
@click.option(
    '-dmov', '--destination-mov', 'dst_path_mov',
    type=click.Path(),
    default='~/Media', show_default=True,
    help='The target directory to sort to: movies ONLY, shadows the --destination option'
)
@click.option(
    '-t', '--type', 'mediatype',
    type=click.Choice([t.value for t in MediaType]),
    default='auto', show_default=True,
    help='The type of media to aid the sorter'
)
@click.option(
    '-a', '--action', 'action',
    type=click.Choice([a.value for a in Action]),
    default='copy', show_default=True,
    help='How to get the media to the destination'
)
@click.option(
    '-i/-I', '--infofile/--no-infofile', 'infofile',
    is_flag=True, default=False, show_default=True,
    help="Create information file at target."
)
@click.option(
    '-s/-S', '--shasum/--no-shasum', 'shasum',
    is_flag=True, default=False, show_default=True,
    help="Create SHA256sum file at target."
)
@click.option(
    '-o/-O', '--chown/--no-chown', 'chown',
    is_flag=True, default=False, show_default=True,
    help="Change ownership and permissions of destfile to match user/group and mode."
)
@click.option(
    '-u', '--user', 'user',
    default='root', show_default=True,
    help='The user that should own the sorted files if --chown'
)
@click.option(
    '-g', '--group', 'group',
    default='media', show_default=True,
    help='The group that should own the sorted files if --chown'
)
@click.option(
    '-mf', '--file-mode', 'file_mode',
    default='0o644', show_default=True,
    help='The Python-octal-format permissions for the target files if --chown'
)
@click.option(
    '-md', '--directory-mode', 'directory_mode',
    default='0o755', show_default=True,
    help='The Python-octal-format permissions for the created file parent directory if --chown'
)
@click.option(
    '-tm', '--tag-metainfo', 'metainfo_tag',
    is_flag=True, default=False, show_default=True,
    help="Add metainfo tagging to target filenames (see README)."
)
@click.option(
    '-o', '--overwrite', 'overwrite',
    is_flag=True, default=False, show_default=True,
    help='Replace files at the destination'
)
@click.option(
    '-x', '--dryrun', 'dryrun',
    is_flag=True, default=False,
    help='Don\'t perform actual sorting'
)
@click.option(
    '-c', '--config', 'config_file',
    envvar='MEDIASORTER_CONFIG',
    type=click.Path(),
    default='/etc/moviesorter/moviesorter.yml', show_default=False,
    help="Override default configuration file path."
)
@click.option(
    '-v', '--verbose', 'verbose',
    is_flag=True, default=False,
    help="Show INFO messages."
)
@click.option(
    '-vv', 'extra_verbose',
    is_flag=True, default=False,
    help="Show DEBUG messages."
)
@click.option(
    '-q', '--quiet', 'quiet',
    is_flag=True, default=False,
    help="No console ouput. (!) Performs sorting operations without asking."
)
@click.option(
    '-y', '--yes', 'yes',
    is_flag=True, default=False,
    help="Don't ask for confirmation."
)
@click.option(
    '-l', '--logfile', required=False,
    help="Log to file (overrides the configuration option)."
)
@click.option(
    '--loglevel', required=False, default="INFO",
    help="Specify log level for the file handler (overrides the configuration option)."
)
@click.argument(
    'src_paths', required=False, nargs=-1,
)
def cli_root(
        src_paths, dst_path, mediatype, action, infofile, shasum, chown, user, group, file_mode,
        directory_mode, metainfo_tag, dryrun, config_file, logfile, loglevel,
        verbose, extra_verbose, quiet, yes, overwrite, dst_path_mov, dst_path_tv
):
    """
    Sort the file or directory SRC PATH.
    """

    console = Console(quiet=quiet)

    config = _load_config(console=console, config_file=config_file, verbose=verbose) or sys.exit(1)

    # Set up (restrict) logging to console...
    if verbose:
        console_log_level = logging.INFO
    elif extra_verbose:
        console_log_level = logging.DEBUG
    else:
        console_log_level = logging.CRITICAL

    for h in logging.getLogger().handlers:
        h.setLevel(console_log_level)

    # ...and to a file.
    if log_file := logfile or config.logfile:
        log.debug(f"Setting up logging to '{log_file}'")
        try:
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(
                logging.Formatter("%(asctime)s [%(module)s] [%(levelname)s] %(message)s")
            )
            file_handler.setLevel(loglevel or config.loglevel or 'INFO')
            logging.getLogger().addHandler(file_handler)
        except PermissionError:
            console.print(Text(f"Can't log to file '{log_file}', permission denied.", style="red"))

    if src_paths:
        # Sort TV and movie medias to their respective directories if corresponding options
        # are specified ('dst_path_tv' and 'dst_path_mov' respectively) and if 'media type'
        # allows it. Otherwise, use the same path (dst_path) for both media types.
        dst_path = os.path.abspath(os.path.expanduser(dst_path))
        dst_path_tv = os.path.abspath(os.path.expanduser(dst_path_tv)) if dst_path_tv else dst_path
        dst_path_mov = os.path.abspath(os.path.expanduser(dst_path_mov)) if dst_path_mov else dst_path
        sorters = [
            MediaSorter(
                config,
                source_path=os.path.abspath(os.path.expanduser(src_path)),
                restrict_media_type=MediaType(mediatype),
                tv_show_destination=dst_path_tv if mediatype in ("tv", "auto") else None,
                movies_destination=dst_path_mov if mediatype in ("movie", "auto") else None,
                allow_metainfo_tagging=metainfo_tag
            ) for src_path in src_paths
        ]
    elif config.scan_sources:
        # If no source path is specified on CLI, grab all scan directories from the configuration.
        sorters = [
            MediaSorter(
                config,
                source_path=sc.src_path,
                restrict_media_type=MediaType(sc.force_type),
                tv_show_destination=sc.tv_shows_output if sc.force_type in ("tv", "auto") else None,
                movies_destination=sc.movies_output if sc.force_type in ("movie", "auto") else None,
                allow_metainfo_tagging=metainfo_tag
            ) for sc in config.scan_sources
        ]
    else:
        console.print(Text("No scans requested.", style="bold red"))
        log.error("No scans requested.")
        sys.exit(1)

    # Iterate through the source path and grab available sorting operations.
    s = console.status(Text("Scanning", style="green bold"))
    if not verbose and not extra_verbose:
        s.start()

    batches: List[Tuple[MediaSorter, List[Operation]]] = []
    for sorter in sorters:
        line = f"scanning {sorter.source_path}"
        log.info(f"+{'-' * (len(line) + 4 + 4)}+")
        log.info(f"|{' ' * 4}scanning {sorter.source_path}{' ' * 4}|")
        log.info(f"+{'-' * (len(line) + 4 + 4)}+")

        ops = asyncio.run(sorter.scan())
        for op in ops:
            # TODO: move to sorter
            op.action = Action(action)
        batches.append((sorter, ops))

    s.stop()

    # Go through all the 'batches' one by one (ask for confirmation if needed).
    batch_index = 1
    exit_code = 0
    for sorter, ops in batches:
        # Print pre-sort summary.
        console.print()
        console.print(
            Text(f"Batch {batch_index}/{len(batches)} ({sorter.source_path})", style="green")
        )
        console.rule(style="green")
        batch_index += 1
        ops = sorted(ops, key=lambda o: o.state, reverse=True)
        for sort_operation in ops:
            _pretty_print_operation(sort_operation, console, before=True, verbose=verbose)

        to_be_sorted = [o for o in ops if not o.is_error]
        errored = [o for o in ops if o.is_error]

        console.print(
            Text(f"\nOK: {len(to_be_sorted)}", style="green"),
            Text(","),
            Text(f"SKIP: {len(errored)}", style="red" if errored else "green"),
        )

        console.rule(style="red" if any([op.is_error for op in ops]) else "green")

        if not to_be_sorted:
            if errored:
                log.error(
                    f"No valid files for sorting in: '{sorter.source_path}', "
                    f"{len(errored)} errors."
                )
                console.print(Text("Nothing to sort!", style="bold red"))
                exit_code = 1
            else:
                log.info(f"Nothing to sort in: '{sorter.source_path}'.")
                console.print(Text("Nothing to sort.", style="green bold"))
            continue

        if dryrun:
            log.info("--dryrun, we're done here.")
            continue

        confirmed = yes or quiet or Confirm.ask("Continue?")

        if not confirmed:
            continue

        # SORT!
        for op in to_be_sorted:
            op.action = Action(action)
        completed_operations = asyncio.run(sorter.commit_all(
            to_be_sorted,
            user=user,
            group=group,
            chown=chown,
            infofile=infofile,
            shasum=shasum,
            file_mode=file_mode,
            dir_mode=directory_mode,
            overwrite=overwrite
        ))

        for sort_operation in completed_operations:
            _pretty_print_operation(sort_operation, console, verbose=verbose)

        # Return non-zero if any of the confirmed sort operations fails.
        if any([op.is_error for op in completed_operations]):
            exit_code = 1

    sys.exit(exit_code)


def main():
    cli_root(obj={})


if __name__ == "__main__":
    main()
