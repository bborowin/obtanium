#!/usr/bin/python

from elixir import *
from time import sleep
import prowlpy
from operations.find import search
from operations.notify import Notifier


metadata.bind = "mysql://obtanium:obtanium@localhost/obtanium?charset=utf8"
setup_all()

nt = Notifier()
while(True):
    try:
        session.commit()
        search()
        nt.send()
    except Exception as e:
        print e
    sleep(5)
