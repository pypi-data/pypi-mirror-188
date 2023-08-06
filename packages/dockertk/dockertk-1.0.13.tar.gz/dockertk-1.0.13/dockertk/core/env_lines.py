
from ..utils import get_indent,from_first_letter


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
            elif ":" in ffl:
                lhs, rhs = ffl.split(":", 1)
                ffl = f"{lhs.rstrip()}={rhs.lstrip()}"
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

