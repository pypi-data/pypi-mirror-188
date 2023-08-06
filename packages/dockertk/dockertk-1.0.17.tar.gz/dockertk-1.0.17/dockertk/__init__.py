from .core import env_dict
from .core import env_src
from .utils import dict_utils
from .utils import path_utils

def docker_compose_dict(path: str):
    return env_dict.env_dict(path=path, env=env_dict.EnvType.DOCKER_COMPOSE)

def dotenv_dict(path: str):
    return env_dict.env_dict(path=path, env=env_dict.EnvType.DOTENV)

def dockerfile_dict(path: str):
    return env_dict.env_dict(path=path, env=env_dict.EnvType.DOCKERFILE)


from dataclasses import dataclass

@dataclass(frozen=False,order=True)
class EnvPaths:
    docker_compose_path: str
    dotenv_path: str
    dockerfile_path: str
    python_env_path: str



def unified_environment(env_paths:EnvPaths):
    result = {}
    path = env_paths.docker_compose_path
    if path_utils.path_exists(path):
        docker_compose_env = docker_compose_dict(path=path)
        result = dict_utils.safe_merge(result,docker_compose_env)
    path = env_paths.dockerfile_path
    if path_utils.path_exists(path):
        dockerfile_env = dockerfile_dict(path)
        result = dict_utils.safe_merge(result,dockerfile_env)
    path = env_paths.dotenv_path
    if path_utils.path_exists(path):
        dotenv_env = dotenv_dict(path)
        result = dict_utils.safe_merge(result,dotenv_env)
    return result

def refresh_envs(
    docker_compose_path: str = "docker-compose.yml",
    dotenv_path: str = ".env",
    dockerfile_path: str = "Dockerfile",
    python_env_path: str = "env.py",
):

    env_paths = EnvPaths(
        **dict(
            docker_compose_path=docker_compose_path,
            dotenv_path=dotenv_path,
            dockerfile_path=dockerfile_path,
            python_env_path=python_env_path
        )
    )
    env = unified_environment(env_paths=env_paths)

    if env:
        dotenv_src = env_src.form_dotenv_src(env)
        python_src = env_src.form_python_env_src(env=env, dotenv_path=dotenv_path,python_env_path=python_env_path)
        dockerfile_src = env_src.form_dockerfile_env_src(env, dockerfile_path)
        path_utils.write_text(dotenv_path, dotenv_src)
        path_utils.write_text(python_env_path, python_src)
        path_utils.write_text(dockerfile_path, dockerfile_src)
