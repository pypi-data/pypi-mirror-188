import os
import math

import pandas as pd
import matplotlib.pyplot as plt

from .constants.interval import Interval
from .constants.definitions import * 


def resampling_based_on_time_frame(source_df: pd.DataFrame, source_interval: Interval, destination_interval: Interval):
    """_summary_

    Args:
        source_df (pd.DataFrame): _description_
        source_interval (Interval): _description_
        destination_interval (Interval): _description_

    Returns:
        _type_: _description_
    """
    step = int(destination_interval / source_interval)

    df = source_df.copy()
    df['open'] = df.open.rolling(step).agg(lambda w: w.iloc[0]).shift(-step + 1)
    df['high'] = df.high.rolling(step).max().shift(-step + 1)
    df['low'] = df.low.rolling(step).min().shift(-step + 1)
    df['close'] = df.close.rolling(step).agg(lambda w: w.iloc[-1]).shift(-step + 1)
    df['volume'] = df.volume.rolling(step).sum().shift(-step + 1)

    df = df.dropna() # drop last nan rows
    df = df[(0 == df.timestamp % destination_interval)] # keep destination interval rows and drop extra rows 
    df = df.reset_index(drop=True) # reset index to zero and drop previous indices
    
    return df