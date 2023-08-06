from copyright_cli import internal
import logging
import pathlib
import shutil


_logger = logging.getLogger(__name__)


def add_copyright(config_path, output_path, skip_if_exists=True):
    _logger.debug("Running add_copyright")

    config = internal.Configuration.load(config_path, ".copyright")

    if output_path is None:
        output_path = str(config.root_path)

    _logger.debug(f" - output_path = {output_path}")

    for folder in config.search_folders:
        _logger.debug(f"Searching in = {folder}")

        files = internal.FileSearch.run(config.root_path, [folder], config.file_extensions, False)
        _logger.debug(f" - Found {len(files)} files")

        for file_path in files:
            input_file_path = str(pathlib.Path(config.root_path).joinpath(file_path))

            _logger.debug(f" - Processing {input_file_path}")

            has_copyright = False
            if skip_if_exists:
                _logger.debug(f" -- Checking if copyright already exists")
                has_copyright = internal.FileProcessor.has_copyright(input_file_path, config.copyright_info)

            output_file_path = pathlib.Path(output_path).joinpath(file_path)
            if has_copyright:
                _logger.debug(f" -- Copyright already detected. Adding copyright will be skipped")
                if not output_file_path.exists():
                    shutil.copyfile(input_file_path, str(output_file_path))
            else:
                _logger.debug(f" -- Adding copyright")
                internal.FileProcessor.add_copyright_to_file(input_file_path, str(output_file_path), config.copyright_info)
