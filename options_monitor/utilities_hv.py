# encoding: UTF-8

import pandas as pd
import numpy as np


HV_20_NAME = 'hv20'
HV_250_NAME = 'hv250'
HV_20_250_NAME = 'hv20/250'
HV_PER = 'per'
# about 1 years
HV_DISTRIBUTION_PERIODS = 250


#----------------------------------------------------------------------
def historical_volatility(close: pd.Series, n: int):
    """calculate the historical volatility"""
    # NYSE = 252 trading days; Shanghai Stock Exchange = 242; Tokyo Stock Exchange = 246 days?
    # options strategy use 260
    log_close = np.log(close / np.roll(close, 1))
    log_close[0] = np.nan
    return np.sqrt(np.multiply(HV_DISTRIBUTION_PERIODS, log_close.rolling(n).var()))


#----------------------------------------------------------------------
def index_distribution_of_per(size: int):
    """calculate the index to split a list"""
    min_delta = int(np.floor(size / 100))
    remain = size - min_delta * 100
    # remain to the bottom
    li = []
    for idx in range(99):
        delta = min_delta
        if remain > 0:
            delta += 1
            remain -= 1
        if 0 == idx:
            li.append(delta)
        else:
            li.append(li[-1] + delta)
    return li


#----------------------------------------------------------------------
def percent_distribution_list(hvs: pd.Series):
    """calculate the percentage value list"""
    sorted_hvs = hvs.dropna().sort_values()
    size = sorted_hvs.shape[0]
    if size < HV_DISTRIBUTION_PERIODS:
        # not enough size,  return empty list
        return []
    else:
        sorted_hvs = sorted_hvs[-HV_DISTRIBUTION_PERIODS:]
        idxes = index_distribution_of_per(HV_DISTRIBUTION_PERIODS)
        return map(lambda idx: sorted_hvs.iloc[idx], idxes)


#----------------------------------------------------------------------
def percent_distribution(vix: pd.Series, val: float = None):
    """calculate the percentage of the value at"""
    dis = percent_distribution_list(vix)
    if [] == dis:
        # not enough distribution, return 50
        return 50
    if val is None:
        val = vix.iloc[-1]
    ret = 0
    for tval in dis:
        if val > tval:
            ret += 1
        else:
            break
    return ret


#----------------------------------------------------------------------
def calc_percentage(hv_20: pd.Series):
    """"""
    return hv_20.rolling(HV_DISTRIBUTION_PERIODS).apply(lambda rows: percent_distribution(rows))
