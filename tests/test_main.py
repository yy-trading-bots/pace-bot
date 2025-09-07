# tests/test_main.py
import importlib
import runpy
import sys
import types
from typing import Any, cast


def _install_dummy_pacebot(monkeypatch, calls):
    bot_pkg = types.ModuleType("bot")
    bot_pkg.__path__ = []  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, "bot", bot_pkg)

    pace_bot_mod = types.ModuleType("bot.pace_bot")

    class DummyPaceBot:
        def __init__(self):
            calls.append("init")

        def run(self):
            calls.append("run")

    cast(Any, pace_bot_mod).PaceBot = DummyPaceBot  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, "bot.pace_bot", pace_bot_mod)


def test_main_function_calls_pacebot_run(monkeypatch):
    calls = []
    _install_dummy_pacebot(monkeypatch, calls)
    mod = importlib.import_module("main")
    importlib.reload(mod)
    mod.main()
    assert calls == ["init", "run"]


def test_module_runs_when_invoked_as_script(monkeypatch):
    calls = []
    _install_dummy_pacebot(monkeypatch, calls)
    runpy.run_module("main", run_name="__main__")
    assert calls == ["init", "run"]
