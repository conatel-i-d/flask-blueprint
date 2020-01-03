import os
from alembic.config import Config
from alembic import command

from app import create_app

FLASK_ENV = os.environ.get('FLASK_ENV', 'dev')
FLASK_PORT = os.environ.get('FLASK_PORT', '8080')
FLASK_HOST = os.environ.get('FLASK_HOST', '0.0.0.0')

alembic_cfg = Config('./alembic.ini')

if FLASK_ENV == 'prod':
    DATABASE_URI = os.environ.get('DATABASE_URI', '')
    alembic_cfg.set_main_option('slqalchemy.url', DATABASE_URI)

(app, _) = create_app(FLASK_ENV)

if __name__ == '__main__':
    command.upgrade(alembic_cfg, "head")
    app.run(host=FLASK_HOST, port=FLASK_PORT)

