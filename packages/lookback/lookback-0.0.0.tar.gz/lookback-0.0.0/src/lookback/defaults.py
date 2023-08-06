"""Defaults"""

import json
from pathlib import Path

from lookback import board
from lookback.configs import get_config

config = get_config()


def load_boards(path: Path) -> list[board.Model]:
    """Load Trello boards."""
    return [
        load_board(path)
        for path in path.glob("*.json")
        if config.skip_boards and path.stem not in config.skip_boards
    ]


def load_board(path: Path) -> board.Model:
    """Load a Trello board."""
    return board.Model(**json.loads(path.read_text(encoding="utf-8")))


boards = load_boards(config.boards)
