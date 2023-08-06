"""Configure lookback."""

from pathlib import Path
import tomllib

from pydantic import BaseModel, DirectoryPath, Extra, Field

APPDIR = Path("~/.lookback").expanduser()


def init():
    """Initialize the application."""
    APPDIR.mkdir(exist_ok=True)
    generate_schema()


class MyBaseModel(BaseModel):
    class Config:
        """Model configuration"""

        extra = Extra.forbid  # To forbid extra fields


class AppConfig(MyBaseModel):
    """Application configuration."""

    boards: DirectoryPath = Field(
        ..., description="Directory containing exported Trello baords."
    )
    skip_boards: list[str] | None = Field(None, description="Boards IDs to skip.")
    reports: DirectoryPath = Field(
        ..., description="Directory to store generated reports."
    )


def get_config():
    """Get default configuration."""
    config = APPDIR / "config.toml"
    return AppConfig(**tomllib.loads(config.read_text(encoding="utf-8")))


def generate_schema():
    """Write the configuration schema."""
    schema = APPDIR / "config-schema.json"
    schema.write_text(AppConfig.schema_json(indent=2) + "\n", encoding="utf-8")
