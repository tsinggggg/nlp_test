from pathlib import Path
import os


def get_config(file_name) -> Path:
    """Returns the path a config file.
    Returns:
        The path to a config file.
    """
    return Path(__file__).parent.parent / "nlptest" / file_name


def get_config_default():
    """Returns the path to the default config file.
    Returns:
        The path to the default config file.
    """
    return Path(__file__).parent.parent / "nlptest/config_default.yaml"


def set_cache_dir(cache_dir):
    os.environ["TA_CACHE_DIR"] = cache_dir
    try:
        os.makedirs(cache_dir)
    except FileExistsError:  # cache path exists
        pass
