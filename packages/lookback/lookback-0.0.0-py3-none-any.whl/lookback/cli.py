"""CLI"""

from datetime import datetime
from pathlib import Path

from datamodel_code_generator import InputFileType, PythonVersion, generate
import pyperclip
from typer import Typer

from lookback import api, configs
from lookback.defaults import boards, config

app = Typer()

now = datetime.now()
REPORT = Path(
    config.reports / f"{now.replace(microsecond=0).isoformat().replace(':', '-')}.md"
)


@app.command()
def generate_report(days: int = 8, output: Path = REPORT):
    """Generate a report from comments."""
    report: str = ""
    for board in boards:
        comments = api.get_comments(board)
        comments = api.filter_comments(comments, days=days)
        cards = {
            comment.data.card.name
            for comment in comments
            if comment.data.card and comment.data.card.name
        }
        comments_by_card = [api.filter_comments(comments, card=card) for card in cards]
        comments_in_cards = {
            card: api.sort_comments(comments)
            for card, comments in zip(cards, comments_by_card)
        }
        if comments:
            report += f"# {board.name}\n\n"
        for card, comments in comments_in_cards.items():
            comments = api.agg_comments(comments)
            report += f"## {card}\n\n"
            report += "\n\n".join([comment.data.text for comment in comments])
            report += "\n\n"
        output.write_text(report, encoding="utf-8")


@app.command()
def get_comments(
    board: str,
    card: str,
    days: int = 0,
):
    """Get comments from a card."""
    comments = api.get_comments([b for b in boards if b.name == board][0])
    filtered_comments = api.filter_comments(comments, card, days)
    pyperclip.copy("\n\n\n".join([comment.data.text for comment in filtered_comments]))


# * -------------------------------------------------------------------------------- * #
# * BACKEND


@app.command()
def generate_model(input_file: Path, output_file: Path):
    """Generate data model from JSON file."""
    generate(
        input_file,
        output=output_file,
        input_file_type=InputFileType.Json,
        snake_case_field=True,
        target_python_version=PythonVersion.PY_311,
    )


@app.command()
def generate_schema():
    """Generate configuration schema."""
    configs.generate_schema()
