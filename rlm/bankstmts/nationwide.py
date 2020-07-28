import pandas as pd
import numpy as np
import logging
gumpf_rows = 4

log = logging.getLogger(__name__)


def read_tx_file(fpath):
    """
    Read a single file of transactions, stripping currency signs out and converting numeric columns to numeric data
    types.
    :param fpath: path to transaction file.
    :return: pd.DataFrame
    """
    df = pd.read_csv(fpath,
                     infer_datetime_format=True,
                     parse_dates=[0],
                     skiprows=gumpf_rows,
                     encoding='latin1')
    df.rename(columns={
        'Paid out': 'out_str',
        'Paid in': 'in_str',
        'Balance': 'balance_str',
    }, inplace=True)
    log.info('    - read {:d} transactions from \'{}\''.format(len(df), fpath))
    for c in ['out', 'in', 'balance']:
        if df[c + '_str'].isnull().all():
            df[c] = np.nan
        else:
            df[c] = df[c + '_str'].str.replace(r'[^-+\d.]', '').astype(float)  # decimal.Decimal)

    return df.drop(['out_str', 'in_str', 'balance_str'], axis='columns')


