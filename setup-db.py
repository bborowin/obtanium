#!/usr/bin/python
import config as config
import sqlalchemy, elixir

elixir.options_defaults.update(dict(
    tablename = lambda cls: cls.__name__.lower(),
    table_options = dict(
        mysql_engine = "InnoDB",
        mysql_collate = "utf8_general_ci"
    ),
    polymorphic = True,
    inheritance = 'multi'
))

from models.remote import *
from models.local import *

binding = config.get('config')['db']['connection']
metadata.bind = sqlalchemy.create_engine(binding, pool_recycle=3600)
setup_all()

setup_all()
create_all()

