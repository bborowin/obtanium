#!/usr/bin/python
from elixir import *
from models.remote import *
from models.local import *
metadata.bind = "mysql://obtanium:obtanium@localhost/obtanium"
setup_all()
create_all()
