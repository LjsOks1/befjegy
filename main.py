#!/usr/bin/python
# -*- coding: utf-8 -*-
from  befjegy import befjegy
from graph import graph
import numpy
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import csv

befjegy.refresh_isin()
x=befjegy.from_file("isin.conf")
#x=befjegy(["HU0000709092"])
#x=befjegy.from_file("reszvenyek.conf")
#x.refresh_isin()
#df=x.get_overview()

#result=x.get_yield_array("1yyield")
#result=x.get_asset_value()
#y=graph("OTP Részvény Alap - Árfolyam").show(x.get_trades())
#y=graph("Mean - StdDev").show_scatter(x.get_overview("1yyield"))
#y=graph("OTP Reszveny Alapok").show_boxplot(x.get_yields_array("1yyield"))

#y=graph("1y yields").show_hist(x.get_yields("1yyield"))
#y=graph("Részvények - Forgalom", x.get_trades())
