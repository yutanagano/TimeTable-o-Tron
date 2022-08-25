from pathlib import Path


def resolve_path_to_new_timetable(str_path: str) -> Path:
    path = Path(str_path).resolve()

    if path.is_file() and path.suffix == '.xlsx':
        return path

    raise RuntimeError(
        f'new_timetable should be an existing .xlsx file. Got: {str_path}'
    )


def resolve_path_to_old_timetables(str_path: str) -> Path:
    path = Path(str_path).resolve()

    if path.is_dir():
       return path

    raise RuntimeError(
        f'old_timetable_dir should be an existing directory. Got: {str_path}'
    ) 