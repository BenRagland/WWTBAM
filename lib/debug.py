#!/usr/bin/env python3
# lib/debug.py

from models.__init__ import CONN, CURSOR
from models.users import Users
from models.question import Question
from models.game import Game

import ipdb

Question.create_table()

question1 = Question("What is the chemical symbol for gold?", ["Au", "Ag", "Cu", "Fe"], "Au", {"difficulty": "Easy"})

ipdb.set_trace()