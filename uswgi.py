import os

from app import create_app
from alembic.config import Config
from alembic import command

alembic_cfg = Config("./alembic.ini")
alembic_cfg.set_main_option('sqlalchemy.url', os.environ['DATABASE_URI'])
command.upgrade(alembic_cfg, "head")

(app, _) = create_app("prod")
