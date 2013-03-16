#!/usr/bin/python

from elixir import *
from time import sleep
import prowlpy
import db
db.init()

from operations.find import search
from operations.notify import Notifier

nt = Notifier()
while(True):
    try:
        session.commit()
        search()
        nt.send()
    except Exception as e:
        print e
    sleep(5)
