from datetime import date, timedelta
from typing import Tuple


def get_day(days_back=0) -> Tuple[str, date]:
    today = date.today() - timedelta(days=days_back)
    return today.strftime("%Y%m%d"), today


def replace_line(file_name: str, line_num: int, text: str) -> None:
    lines = open(file_name, "r").readlines()
    lines[line_num] = text
    with open(file_name, "w") as out:
        out.writelines(lines)
