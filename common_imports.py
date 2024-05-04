# Common libraries used across the project

import yfinance as yf
import pandas_datareader.data as pdr
import pandas as pd
import numpy as np

import datetime
from datetime import datetime, timedelta, date

import time
from dateutil.relativedelta import relativedelta

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.dates import AutoDateLocator, AutoDateFormatter

import tkinter as tk
from PIL import Image, ImageTk

from cachetools import cached, LRUCache
