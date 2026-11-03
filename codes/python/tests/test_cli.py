import subprocess
import sys
import pytest


def test_cli_help():
    res = subprocess.run([sys.executable, "-m", "battery_toolkit.cli", "--help"], capture_output=True, text=True)
    assert res.returncode == 0
    assert "Battery Systems Technology CLI Toolkit" in res.stdout


def test_cli_convert():
    res = subprocess.run([sys.executable, "-m", "battery_toolkit.cli", "convert", "--kw", "100"], capture_output=True, text=True)
    assert res.returncode == 0
    assert "134.10 HP" in res.stdout


def test_cli_size():
    res = subprocess.run([sys.executable, "-m", "battery_toolkit.cli", "size", "--voltage", "400", "--energy", "60"], capture_output=True, text=True)
    assert res.returncode == 0
    assert "Topology" in res.stdout
    assert "Total Cells" in res.stdout
