from typing import Dict
from ..utils import path_utils

def form_dotenv_src(__dict: Dict[str, str]):
    env_lines = [f"{key}={value}" for key, value in __dict.items()]
    env_lines.sort()
    return "\n".join(env_lines) if env_lines else ""


def form_python_env_src(env: Dict[str, str], dotenv_path: str = ".env",python_env_path:str="env.py"):

    field_src = lambda key: f"    {key}:Optional[str] = Field(default=None)"
    keys = list(env.keys())
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

    if path_utils.path_exists(python_env_path):
        env_src = path_utils.read_text(python_env_path)
        if env_init_src in env_src:
            env_src = env_init_src.split(env_init_src,1)[1]
            result += f"\n{env_src}"
    return result


def form_dockerfile_env_src(
    __dict: Dict[str, str], dockerfile_path: str = "Dockerfile"
):
    dockerfile_lines = []
    if path_utils.path_exists(dockerfile_path):
        dockerfile_env_src = path_utils.read_text(dockerfile_path)
        dockerfile_lines = dockerfile_env_src.splitlines(keepends=False)
    dockerfile_lines = [line for line in dockerfile_lines if not line.startswith("ENV")]
    endline = ""
    if dockerfile_lines:
        endline = dockerfile_lines[-1]
        dockerfile_lines = dockerfile_lines[:-1]
    env_lines = [f"ENV {key}={value}" for key, value in __dict.items()]
    result = dockerfile_lines + env_lines + [endline]
    return "\n".join(result)
