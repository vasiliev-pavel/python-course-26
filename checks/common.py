"""Общие инструменты проверок. НЕ МЕНЯТЬ."""

import ast
import importlib.util
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

passed = 0
failed = 0

# Модули команд, которые импортируют друг друга по короткому имени (from fight import battle).
# Перед загрузкой файлов другой команды их нужно «забыть», иначе подхватится чужой fight.py.
TEAM_MODULES = ["items", "fight", "location", "storage", "team_classes"]


def ok(what, actual, expected):
    """Сравнить результат с ожидаемым и напечатать OK или FAIL."""
    global passed, failed
    if isinstance(expected, float) and isinstance(actual, (int, float)) and not isinstance(actual, bool):
        good = abs(actual - expected) < 0.01
    else:
        good = actual == expected and type(actual) == type(expected)
    if good:
        passed += 1
        print(f"OK    {what}")
    else:
        failed += 1
        print(f"FAIL  {what}  ожидалось {expected!r}, получено {actual!r}")


def fail(what, reason):
    global failed
    failed += 1
    print(f"FAIL  {what}  {reason}")


def team_dir(team):
    return os.path.join(ROOT, "teams", team)


def team_file(team, name):
    return os.path.join(team_dir(team), name)


def constants(path):
    """Константы файла: строки вида NAME = "текст" или NAME = 42 на верхнем уровне."""
    with open(path, encoding="utf-8") as f:
        tree = ast.parse(f.read())
    result = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            try:
                result[node.targets[0].id] = ast.literal_eval(node.value)
            except ValueError:
                pass
    return result


def run_script(path, inputs):
    """Запустить программу, подать ей ввод (каждый элемент — строка ввода). Вернуть всё, что она напечатала."""
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    try:
        done = subprocess.run(
            [sys.executable, path], input="\n".join(inputs) + "\n", capture_output=True,
            text=True, encoding="utf-8", timeout=10, env=env, cwd=os.path.dirname(path),
        )
    except subprocess.TimeoutExpired:
        return "<программа не закончилась за 10 секунд: возможно, бесконечный цикл>"
    output = done.stdout
    if done.returncode != 0:
        last = done.stderr.strip().splitlines()[-1:] or ["?"]
        output += f"\n<ошибка: {last[0]}>"
    return output


def printed(what, output, text):
    """Проверить, что программа напечатала text (целиком, не частью большего числа)."""
    global passed, failed
    pattern = re.escape(text) + (r"(?![\d.])" if text[-1:].isdigit() else "")
    if re.search(pattern, output):
        passed += 1
        print(f"OK    {what}")
    else:
        failed += 1
        tail = output.strip().replace("\n", " | ")
        if len(tail) > 300:
            tail = "..." + tail[-300:]
        print(f"FAIL  {what}  ожидалась строка {text!r}")
        print(f"      программа напечатала: {tail}")


def not_printed(what, output, text):
    global passed, failed
    if text in output:
        failed += 1
        print(f"FAIL  {what}  строки {text!r} быть не должно")
    else:
        passed += 1
        print(f"OK    {what}")


def load(team, name):
    """Загрузить файл команды как модуль. Если не получилось — None и FAIL с причиной."""
    path = team_file(team, name + ".py")
    if not os.path.exists(path):
        fail(f"{name}.py", f"нет файла teams/{team}/{name}.py")
        return None
    for mod in TEAM_MODULES:
        sys.modules.pop(mod, None)
    sys.path.insert(0, team_dir(team))
    if ROOT not in sys.path:
        sys.path.append(ROOT)
    try:
        spec = importlib.util.spec_from_file_location(f"{team}_{name}", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    except Exception as e:
        fail(f"{name}.py", f"файл не загружается: {type(e).__name__}: {e}")
        return None
    finally:
        sys.path.remove(team_dir(team))


def call(what, function, *args):
    """Вызвать функцию; если она упала — FAIL с причиной и None."""
    try:
        return function(*args)
    except Exception as e:
        fail(what, f"ошибка {type(e).__name__}: {e}")
        return None


def is_placeholder(value):
    return not isinstance(value, str) or value.strip() in ("", "...", "TODO")
