import pandas as pd
from collections.abc import Iterable

def resampler(df, resample, **kwargs) -> pd.DataFrame:

    if resample is None:
        return df
    elif isinstance(resample, Iterable) and not isinstance(resample, str):
        return df.reindex(resample, method='ffill')

    return df.resample(resample, closed='right', label='left', **kwargs).last()

