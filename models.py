import datetime
import pathlib

# orm
from sqlalchemy import Table, Column, Integer, Float, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session


FILES_ROOT_DIR_PATH = pathlib.Path.cwd() / "parsed"


def init_models(db_file_name=None):

    if not FILES_ROOT_DIR_PATH.exists():
        FILES_ROOT_DIR_PATH.mkdir()

    if db_file_name:
        ENGINE = create_engine(f"sqlite:///{FILES_ROOT_DIR_PATH / f'{db_file_name}'}")

    else:
        ENGINE = create_engine(f"sqlite:///{FILES_ROOT_DIR_PATH / f'{datetime.datetime.now()}.db'}")

    SESSION = Session(bind=ENGINE)
    BASE = declarative_base(bind=ENGINE)

    class Unit(BASE):
        __tablename__ = 'unit'

        id = Column(Integer, primary_key=True, autoincrement=True)
        url = Column(Text)
        places = Column(Text)
        price = Column(Float)
        title = Column(Text)

    BASE.metadata.create_all(ENGINE)

    return SESSION, BASE, ENGINE, Unit



