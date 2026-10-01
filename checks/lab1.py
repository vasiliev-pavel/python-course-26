"""Проверки лабы 1. НЕ МЕНЯТЬ."""

from checks.common import constants, fail, is_placeholder, ok, printed, run_script, team_file

import os


def run(team):
    path = team_file(team, "lab1.py")
    if not os.path.exists(path):
        fail("lab1.py", f"нет файла teams/{team}/lab1.py")
        return

    location = constants(path).get("LOCATION_NAME")
    if is_placeholder(location):
        fail("LOCATION_NAME", "придумайте название локации вместо ...")
        location = "..."
    else:
        ok("LOCATION_NAME заполнено", True, True)

    for name, strength, agility, card in [
        ("Артур", 5, 4, [75, 19, 2, "6.0", 6]),
        ("Мира", 2, 9, [60, 18, 4, "13.5", 4]),
    ]:
        out = run_script(path, [name, str(strength), str(agility)])
        hp, attack, defense, speed, points = card
        tag = f"{name}, сила {strength}, ловкость {agility}"
        printed(f"{tag}: заголовок", out, "=== Герой ===")
        printed(f"{tag}: имя", out, f"Имя: {name}")
        printed(f"{tag}: здоровье", out, f"Здоровье: {hp}")
        printed(f"{tag}: атака", out, f"Атака: {attack}")
        printed(f"{tag}: защита", out, f"Защита: {defense}")
        printed(f"{tag}: скорость", out, f"Скорость: {speed}")
        printed(f"{tag}: свободные очки", out, f"Свободных очков: {points}")
        printed(f"{tag}: приветствие", out, f"Добро пожаловать в {location}!")
