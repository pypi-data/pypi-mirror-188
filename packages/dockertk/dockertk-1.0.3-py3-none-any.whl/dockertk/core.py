from enum import Enum
from pathlib import Path
from .util import get_indent, from_first_letter


def path_exists(__path: str):
    return Path(__path).exists()


def read_text(__path: str):
    return Path(__path).read_text()


def write_text(path: str, data: str):
    Path(path).write_text(data=data)


class EnvType(Enum):

    DOTENV = 1
    DOCKERFILE = 2
    DOCKER_COMPOSE = 3
    NONE = 4


def __env_dict_from_lines(__env_lines: list[str]):
    env_lines = __env_lines.copy()
    env_lines.sort()
    env_kv_pairs = [line.split("=", 1) for line in env_lines if "=" in line]
    return {key: value for (key, value) in env_kv_pairs}


def docker_compose_lines(__docker_compose_src: str):
    indent, results = None, []
    for line in __docker_compose_src.splitlines(keepends=False):
        line_indent = get_indent(line)
        if indent is None:
            if line.strip().endswith("environment:"):
                indent = line_indent
        elif line_indent > indent:
            ffl = from_first_letter(line)
            if "=" in ffl:
                results.append(ffl)
        else:
            indent = None
    return results


def dotenv_lines(__src: str):
    return [line for line in __src.splitlines(keepends=False) if "=" in line]


def dockerfile_lines(__src: str):
    return [
        from_first_letter(line.removeprefix("ENV"))
        for line in __src.splitlines(keepends=False)
        if line.lstrip().startswith("ENV") and "=" in line
    ]


def docker_compose_dict(__docker_compose_src: str):
    return __env_dict_from_lines(docker_compose_lines(__docker_compose_src))


def dockerfile_dict(__src: str):
    return __env_dict_from_lines(dockerfile_lines(__src))


def dotenv_dict(__dotenv_src: str):
    return __env_dict_from_lines(dotenv_lines(__dotenv_src))


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
            src = read_text(path)
        result = env_dict(src=src, env=env)
    return result


def form_dotenv_src(__dict: dict[str, str]):
    env_lines = [f"{key}={value}" for key, value in __dict.items()]
    env_lines.sort()
    return "\n".join(env_lines) if env_lines else ""


def form_python_env_src(__dict: dict[str, str], dotenv_path: str = ".env"):
    field_src = lambda key: f"    {key}:Optional[str] = Field(default=None)"
    keys = list(__dict.keys())
    keys.sort()

    env_fields_src = "\n".join(map(field_src, keys))

    env_init_src = "env = Env(**{" + "key:os.environ.get(key) for key in Env.keys()})\n"

    result = f"""
import os
from typing import Optional
from dotenv import load_dotenv
from pydantic import BaseModel, Field

load_dotenv('{dotenv_path}')

class Env(BaseModel):

    @classmethod
    def keys(cls):
        return cls.__fields__.keys()

{env_fields_src}

{env_init_src}

    """
    return result
