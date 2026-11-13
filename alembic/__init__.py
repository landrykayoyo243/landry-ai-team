from alembic import command
from alembic.config import Config
from pathlib import Path

config = Config(str(Path(__file__).resolve().parents[1] / "alembic.ini"))
config.set_main_option("script_location", str(Path(__file__).resolve().parents[1] / "alembic"))
