#!/usr/bin/python

import db
from elixir import create_all

from models.remote import *
from models.local import *

db.init()
create_all()

