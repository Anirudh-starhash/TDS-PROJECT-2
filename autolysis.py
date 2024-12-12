# for connecting with LLM and sending data -> requests and json 
import requests 
import json

# for aiproxy token from environment variables -> os
import os

# ->pandas and numpy for manipulating the dataframe 
import pandas as pd
import numpy as np

# for data visualization -> seaborn
import seaborn as sb

AIPROXY_TOKEN = os.environ["AIPROXY_TOKEN"]


