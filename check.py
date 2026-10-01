"""Проверка лабы.

    python check.py 1 team03     — проверить лабу 1 команды team03

НЕ МЕНЯТЬ. Проверки для новых лаб появляются в папке checks/ вместе с заданием.
"""

import importlib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from checks import common


def main():
    if len(sys.argv) != 3:
        print("Как запускать:  python check.py НОМЕР_ЛАБЫ ПАПКА_КОМАНДЫ")
        print("Например:       python check.py 1 team03")
        return
    lab, team = sys.argv[1], sys.argv[2]
    if not os.path.isdir(common.team_dir(team)):
        print(f"Нет папки teams/{team}. Проверь название команды.")
        return
    try:
        module = importlib.import_module(f"checks.lab{int(lab)}")
    except (ValueError, ModuleNotFoundError):
        print(f"Проверок для лабы {lab} пока нет. Сделай git pull — может, задание уже опубликовано.")
        return
    print(f"Лаба {lab}, команда {team}")
    module.run(team)
    print()
    print(f"Итого: {common.passed} OK, {common.failed} FAIL")
    if common.failed == 0:
        print("Всё готово!")


if __name__ == "__main__":
    main()
