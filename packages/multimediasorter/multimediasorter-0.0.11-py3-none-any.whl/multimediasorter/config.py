import os
from typing import List, Dict, Optional

import yaml
from pydantic import BaseModel, PositiveInt


DEFAULT_CONFIG_PATHS = [
    os.path.expanduser("~/.config/multimediasorter.yml"),
    "/etc/multimediasorter/multimediasorter.yml"
]


class MetadataProviderApi(BaseModel):
    name: str
    key: Optional[str]
    url: Optional[str]
    path: Optional[str]


class ScanConfig(BaseModel):
    """
    Specify an "input/output" combo for different directories
    """
    src_path: str  # source path (duh...)
    force_type: str = "auto"  # force only a specific media type
    tv_shows_output: str  # where to put recognized TV shows
    movies_output: str  # where to put recognized movies


class BaseParams(BaseModel):
    join_character: str = " "  # join char when title has multiple words
    min_split_length: PositiveInt = 3
    suffix_the: bool = False
    search_overrides: Dict[str, str] = {}
    name_overrides: Dict[str, str] = {}
    file_format: str


class MovieParams(BaseParams):
    subdir: bool = True  # sort all files related to a single movie to a common subdir
    file_format = "{title} ({year})"


class TvShowParams(BaseParams):
    dir_format: str = "{series_title}/Season {season_id}"
    file_format: str = '{series_title} - S{season_id:02d}E{episode_id:02d} - {episode_title}'


class Parameters(BaseModel):
    valid_extensions: List[str] = [".avi", ".mkv", ".mp4"]
    split_characters: List[str] = [" ", ".", "_"]
    metainfo_map: List[Dict[str, str]] = {}
    min_split_length: PositiveInt = 3

    tv: TvShowParams = TvShowParams()
    movie: MovieParams = MovieParams()


class Logging(BaseModel):
    logfile: str
    loglevel: str


class Config(BaseModel):
    # Configure different metadata provider APIs (API keys, override URLs,...).
    # Must correspond to an existing key in the MetadataProvider enum.
    api: List[MetadataProviderApi] = []

    # Configure multiple directories to be scanned
    # without the need to specify using command line interface.
    scan_sources: Optional[List[ScanConfig]] = None

    # movie_format: str = "{title} ({year}) - [{metadata}]"
    # tv_show_dir_format: str = "{series_title}/Season {season_id}"
    # tv_show_format: str = '{series_title} - S{season_id:02d}E{episode_id:02d} - {episode_title}'

    parameters: Parameters = Parameters()
    # valid_extensions: List[str] = [".avi", ".mkv", ".mp4"]
    # split_characters: List[str] = [" ", ".", "_"]
    # join_character: str = " "
    # min_split_length: PositiveInt = 3
    # suffix_the: bool = False
    metainfo_map: List[Dict[str, str]] = {}
    # search_overrides: Dict[str, str] = {}
    # tv_name_overrides: Dict[str, str] = {}
    # movie_name_overrides: Dict[str, str] = {}

    loging: Optional[Logging]
    # logfile: Optional[str]
    # loglevel: Optional[str]


def read_config(config_file: str) -> Config:

    with open(config_file, 'r') as cfgfile:
        o_config = yaml.load(cfgfile, Loader=yaml.SafeLoader)

    return Config(**o_config['multimediasorter'])

    # c = Config(
    #     valid_extensions=o_config['multimediasorter']['parameters']['valid_extensions'],
    #     split_characters=o_config['multimediasorter']['parameters']['split_characters'],
    #     min_split_length=int(o_config['multimediasorter']['parameters']['min_split_length']),
    #     suffix_the=o_config['multimediasorter']['parameters']['suffix_the'],
    #     metainfo_map=o_config['multimediasorter']['parameters'].get('metainfo_map', []),
    #     join_character=o_config['multimediasorter']['parameters'].get('join_character', " "),
    #     search_overrides=o_config['multimediasorter'].get('search_overrides', {}),
    #     tv_name_overrides=o_config['multimediasorter'].get('name_overrides', {}).get('tv', {}),
    #     movie_name_overrides=o_config['multimediasorter'].get('name_overrides', {}).get('movie', {}),
    #     log_to_file=o_config['multimediasorter']['logging']['file'],
    #     logfile=o_config['multimediasorter']['logging'].get('logfile'),
    #     loglevel=o_config['multimediasorter']['logging'].get('loglevel'),
    # )
    # if movie_format := o_config['multimediasorter'].get('movie_format'):
    #     c.movie_format = movie_format
    # if tv_show_dir_format := o_config['multimediasorter'].get('tv_show_dir_format'):
    #     c.tv_show_dir_format = tv_show_dir_format
    # if tv_show_format := o_config['multimediasorter'].get('tv_show_format'):
    #     c.tv_show_format = tv_show_format
    #
    # if sources := o_config["multimediasorter"].get("scan_sources"):
    #     c.scan_sources.extend([ScanConfig(**src) for src in sources])
    #
    # for name, config in o_config['multimediasorter'].get('api', {}).items():
    #     c.apis.append(MetadataProviderApi(
    #         name=name,
    #         url=config.get("url"),
    #         key=config.get("key"),
    #         path=config.get("path")
    #     ))
    # return c
