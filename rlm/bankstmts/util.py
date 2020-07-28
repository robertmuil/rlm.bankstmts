import pandas as pd
import logging

log = logging.getLogger(__name__)

def pp(it):
  """
  pretty-print an iterable
  """
  return ", ".join([f"'{str(e)}'" for e in it])


def detect_recurrent_tx(tx: pd.DataFrame, exact: bool = False):
    rv = None

    df = tx.copy()
    df['desc_standard'] = df['Description'].str.lower().str.replace('[^a-zA-Z0-9]', '')


    if not exact:
        raise NotImplementedError
    else:
        # need to use named functions if more than one output per column: https://github.com/pandas-dev/pandas/issues/28467
        def diffdays(d):
                return (d.max() - d.min()).days
        cols_gb = ['out']
        _outs = df.groupby(cols_gb).agg(
                span=pd.NamedAgg(column='Date', aggfunc=diffdays),
                count=pd.NamedAgg(column='Date', aggfunc='count'),
                desc_standard_count=('desc_standard', 'nunique'),
                desc_standard_top3=('desc_standard',
                  lambda s: pp(s.value_counts().sort_values(ascending=False).index[0:3])),
                descriptions=('Description', 'unique'),
        )

        rv = _outs.loc[(_outs['span'] > 0) & (_outs['count'] > 2)].copy()
        rv['period'] = rv['span'] / rv['count']
        rv['count_per_desc'] = rv['count'] / rv['desc_standard_count']

    return rv.sort_values('count_per_desc', ascending=False)
