"""API"""

from datetime import datetime, timedelta

from lookback import board
from lookback.times import end_of_today


def agg_comments(comments: list[board.Action]) -> list[board.Action]:
    """Aggregate comments by their header."""
    misc_heading = "### Miscellaneous"
    texts = [comment.data.text for comment in comments]
    seen: dict[str, board.Action] = {}
    keep: list[bool] = []
    for text, comment in zip(texts, comments):
        (first_line, *rest) = text.split("\n\n")
        if not first_line.startswith("###"):
            first_line = misc_heading
            comment.data.text = f"{first_line}\n\n{comment.data.text}"
        match first_line.split():
            case ["###", *_]:
                if prev_comment := seen.get(first_line):
                    prev_comment.data.text += "\n\n" + "\n\n".join(rest)
                    keep.append(False)
                else:
                    seen[first_line] = comment
                    keep.append(True)
            case _:
                raise ValueError(f"Invalid comment: {comment.data.text}")
    comments = [comment for comment, keep in zip(comments, keep) if keep]
    return sorted(
        comments, key=lambda comment: comment.data.text.startswith(misc_heading)
    )


def sort_comments(comments: list[board.Action]) -> list[board.Action]:
    """Sort comments in chronological order."""
    return sorted(comments, key=lambda comment: datetime.fromisoformat(comment.date))


def filter_comments(comments: list[board.Action], card: str = "", days: int = 0):
    """Filter comments."""
    card_limit = card or None
    date_limit = end_of_today - timedelta(days=days) if days != 0 else None
    return [
        comment
        for comment in comments
        if comment.data.card
        and comment.data.card.name
        and (not card_limit or comment.data.card.name == card)
        and (not date_limit or datetime.fromisoformat(comment.date) > date_limit)
    ]


def get_comments(board: board.Model) -> list[board.Action]:
    """Get comments in chronological order."""
    return [action for action in board.actions if action.type == "commentCard"]
