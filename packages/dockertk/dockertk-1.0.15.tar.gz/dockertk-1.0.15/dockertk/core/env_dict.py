from typing import List
from enum import Enum
from . import env_lines as __env_lines
from ..utils import path_utils
def __env_dict_from_lines(__env_lines: List[str]):
    env_lines = __env_lines.copy()
    env_lines.sort()
    env_kv_pairs = [line.split("=", 1) for line in env_lines if "=" in line]
    return {key: value for (key, value) in env_kv_pairs}



def __env_dict_from_lines(__env_lines: List[str]):
    env_lines = __env_lines.copy()
    env_lines.sort()
    env_kv_pairs = [line.split("=", 1) for line in env_lines if "=" in line]
    return {key: value for (key, value) in env_kv_pairs}



def docker_compose_dict(__docker_compose_src: str):
    return __env_dict_from_lines(__env_lines.docker_compose_lines(__docker_compose_src))


def dockerfile_dict(__src: str):
    return __env_dict_from_lines(__env_lines.dockerfile_lines(__src))


def dotenv_dict(__dotenv_src: str):
    return __env_dict_from_lines(__env_lines.dotenv_lines(__dotenv_src))




class EnvType(Enum):

    DOTENV = 1
    DOCKERFILE = 2
    DOCKER_COMPOSE = 3
    NONE = 4



def env_dict(path: str = None, src: str = None, env: EnvType = EnvType.NONE):
    if src is not None:
        if env == EnvType.DOCKER_COMPOSE:
            result = docker_compose_dict(src)
        elif env == EnvType.DOCKERFILE:
            result = dockerfile_dict(src)
        elif env == EnvType.DOTENV:
            result = dotenv_dict(src)
        else:
            raise Exception(f"unrecognized env_type: {str(env)}")

    else:
        if path is None:
            raise Exception("no param for env_dict")
        else:
            src = path_utils.read_text(path)
        result = env_dict(src=src, env=env)
    return result

