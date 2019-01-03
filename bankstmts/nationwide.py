import pandas as pd
import warnings
import glob

gumpf_rows=4

def read_tx_file(fpath):
    df = pd.read_csv(fpath,
                 infer_datetime_format=True,
                 parse_dates=[0],
                 skiprows=gumpf_rows,
                 encoding='latin1').rename(columns=
                    {
                        'Paid out': 'out_str',
                        'Paid in':  'in_str',
                        'Balance':  'balance_str',
    })
    print('read {:d} transactions from \'{}\''.format(len(df), fpath))
    for c in ['out', 'in', 'balance']:
        df[c] = df[c+'_str'].str.replace(r'[^-+\d.]', '').astype(float)#decimal.Decimal)
    
    return df.drop(['out_str', 'in_str', 'balance_str'], axis='columns')

def read_tx_files(fpath_pattern):
    df_list = []
    fpath_patterns = glob.glob(fpath_pattern)
    for fpath in fpath_patterns:
        df = read_tx_file(fpath)
        df['fpath'] = fpath
        df_list += [df]
    
    if len(df_list) < 1:
        warnings.warn('no files found with pattern \'{}\''.format(fpath_pattern))
        df = None
    else:
        df = pd.concat(df_list).sort_values('Date')
        cols_subset = set(df.columns).difference({'fpath'})
        df = df[~df.duplicated(subset=cols_subset)]
        print('read {:d} unique transactions from {:d} files: from {} to {}'.format(
            len(df),
            len(df_list),
            df.Date.min(),
            df.Date.max()
        ))
    return df

def read_tx_accounts(fpath_patterns):
    df_list = []
    for acct,fpath_pattern in fpath_patterns.items():
        df = read_tx_files(fpath_pattern)
        if df is not None:
            df['account'] = acct
            df_list += [df]
    
    if len(df_list) > 0:
        df = pd.concat(df_list).sort_values('Date')
        print('read {:d} transactions from {:d} accounts: from {} to {}'.format(
            len(df),
            len(df_list),
            df.Date.min(),
            df.Date.max()
        ))
    else:
        df = None
    
    return df
