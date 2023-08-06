from talib import abstract
import numpy as np
import talib
import logging
from collections.abc import Iterable
import sys, traceback
from functools import lru_cache
import pandas as pd
from finlab import data
from typing import List, Protocol, Dict, Optional
import finlab.market_info
from finlab import ml
from finlab.ml.utils import resampler


class IndicatorName():
  
    @staticmethod
    def encode(package_name, func, output, params):

        encoded = package_name + '.' + func + '__' + output + '__'
        for k, v in params.items():
          encoded += f'{k}__{v}__'

        return encoded
    
    @staticmethod
    def decode(encoded):
      
        tokens = encoded.split('__')
        
        func = tokens[0].split('.')[-1]
        output = tokens[1]
        params = dict(zip(tokens[2:][::2], tokens[2:][1::2]))

        return func, output, params


class TalibIndicatorFactory():

    def __init__(self, market:Optional[finlab.market_info.MarketInfo]=None):
        if market:
            self.market = market
        else:
            self.market = ml.market
  
    def calculate_indicator(self, func, output, params, adj=False):
      
        func = func.split('.')[0]

        # get ith output
        f = getattr(abstract, func)
        target_i = -1
        for i, o in enumerate(f.output_names):
            if o == output:
                target_i = i
                break

        if target_i == -1:
            raise Exception("Cannot find output names")
        
        # apply talib
        indicator = data.indicator(func, adj=adj, **params)

        if isinstance(indicator, tuple):
            indicator = indicator[target_i]

        # normalize result
        if func in TalibIndicatorFactory.normalized_funcs():
            indicator /= self.market.get_price('close', adj=adj)

        return indicator
    
    @staticmethod
    def all_functions():
        talib_categories = [
          'Cycle Indicators', 
          'Momentum Indicators', 
          'Overlap Studies', 
          'Price Transform', 
          'Statistic Functions', 
          'Volatility Indicators']

        talib_functions = sum([talib.get_function_groups()[c] for c in talib_categories], [])
        talib_functions = ['talib.'+f for f in talib_functions if f != 'SAREXT' and f != 'MAVP']
        return talib_functions

    @staticmethod
    @lru_cache
    def normalized_funcs():
      talib_normalized = talib.get_function_groups()['Overlap Studies']\
        + talib.get_function_groups()['Price Transform']\
        + ['APO', 'MACD', 'MACDEXT', 'MACDFIX', 'MOM', 'MINUS_DM', 'PLUS_DM', 'HT_PHASOR']
      return ['talib.' + t for t in talib_normalized]
    
    def generate_feature_names(self, func, lb, ub, n):
          
        func = func.split('.')[-1]

        f = getattr(abstract, func)
        outputs = f.output_names
        org_params = f.parameters
        params_lb = {k:v*lb for k, v in org_params.items()}
        params_ub = {k:v*ub for k, v in org_params.items()}
        
        min_value = {
          'signalperiod': 2,
          'timeperiod': 2,
          'fastperiod': 2,
          'slowperiod': 2,
          'timeperiod1': 2, 'timeperiod2': 2,
          'timeperiod3': 2,
          'fastk_period': 2, 
          'fastd_period': 2,
        }

        ret = []
        for _ in range(n):

          new_params = {}
          for k, v in org_params.items():
            rvalue = np.random.random_sample(1)[0] * (params_ub[k] - params_lb[k]) + params_lb[k]
            rvalue = type(v)(rvalue)
            new_params[k] = rvalue
            
          
          if 'nbdevup' in new_params:
            new_params['nbdevup'] = 2
          if 'nbdevdn' in new_params:
            new_params['nbdevdn'] = 2
            
          for p in new_params:
            if p in min_value and new_params[p] < min_value[p]:
              new_params[p] = min_value[p]
            
          for o in outputs:
            ret.append(IndicatorName.encode('talib', func, o, new_params))

        return list(set(ret))

class Factory(Protocol):
    def __init__(self, market:Optional[finlab.market_info.MarketInfo]) -> None:
        pass

    def all_functions(self) -> List[str]:
        return []

    def calculate_indicator(self, func, output, params) -> pd.DataFrame:
        return pd.DataFrame()
 
def generate_ta_names(lb:int=1, ub:int=10, n:int=1, factory=None):

    if factory is None:
        factory = TalibIndicatorFactory()

    return sum([factory.generate_feature_names(f, lb, ub, n) for f in factory.all_functions()], [])

def generate_ta(
        feature_names:Optional[List[str]], 
        factories=dict(talib=TalibIndicatorFactory()), resample=None, **kwargs):

    if feature_names is None:
        feature_names = generate_ta_names()

    features = {}
    for name in feature_names:
        func, output, params = IndicatorName.decode(name)

        factory = factories[name.split('.')[0]]
        try:
            features[name] = resampler(factory.calculate_indicator(func, output, params), resample, **kwargs)
        except Exception as e:
            logging.warn(e)
            traceback.print_exc(file=sys.stdout)
            logging.warn(f"Cannot calculate indicator {name}. Skipped")

    return features


def combine(features:Dict[str, pd.DataFrame], resample=None, **kwargs):

    if len(features) == 0:
        return pd.DataFrame()

    def resampling(df) -> pd.DataFrame:
        return resampler(df, resample, **kwargs).unstack()

    unstacked = {}
    union_index = resampling(next(iter(features.values()))).index

    for name, df in features.items():

        df = df.index_str_to_date()
        udf = resampling(df)
        union_index = union_index.union(udf.index)
        unstacked[name] = udf

    for name in unstacked:
        unstacked[name] = unstacked[name].reindex(union_index).values

    return pd.DataFrame(unstacked, index=union_index)

