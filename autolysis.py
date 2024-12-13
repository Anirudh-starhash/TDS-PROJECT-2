import requests
import json
import os
import pandas as pd
import numpy as np
import seaborn as sns
import argparse
from sklearn.cluster import KMeans

AIPROXY_TOKEN = os.environ["AIPROXY_TOKEN"]



