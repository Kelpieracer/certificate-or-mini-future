import math
import numpy as np
import pandas as pd
from yahoo_fin import stock_info as si
from symbol_dict import symbol_dict
from etp_gain import etp_gain


SIMULATION_LEVERAGE = 5
HOLDING_TIME = 5


def variability(df):
    dfc = df['adjclose'].dropna()
    gains = list([])
    certificate_profits = list([])
    future_profits = list([])
    for today in range(0, len(dfc) - HOLDING_TIME):
        gain = (dfc.iloc[today+HOLDING_TIME] - dfc.iloc[today]) / \
            dfc.iloc[today+HOLDING_TIME]
        if not math.isnan(gain):
            gains.append(abs(gain))
        futu_gain, cert_gain = etp_gain(
            dfc[list(range(today, today + HOLDING_TIME + 1))], SIMULATION_LEVERAGE)
        future_profits.append(max(0, futu_gain))
        certificate_profits.append(max(0, cert_gain))
    for _ in [0, 20]:
        gains.remove(max(gains))
        gains.remove(min(gains))
    ave_change = np.average(gains)
    future_profit = np.average(future_profits)
    certificate_profit = np.average(certificate_profits)
    return ave_change, future_profit, certificate_profit


if __name__ == '__main__':
    start_date = '2012-01-01'
    var_start_date = '2018-01-01'
    results = []
    for ticker_obj in symbol_dict:
        symbol = ticker_obj['symbol']
        if symbol == '':
            continue
        df = si.get_data(symbol, start_date=start_date)
        df['date'] = df.index
        var_df = df.loc[df['date'] >= var_start_date]
        var, futu_gain, cert_gain = variability(var_df)
        results.append(
            {
                'symbol': symbol,
                'variability': var,
                'futu_gain': futu_gain - 1,
                'cert_gain': cert_gain - 1,
                'start_date': df.head(1).index[0].strftime('%Y-%m-%d'),
                'end_date': df.tail(1).index[0].strftime('%Y-%m-%d'),
                'var_start_date': var_df.head(1).index[0].strftime('%Y-%m-%d')})
        print(symbol)
    variabilities = pd.DataFrame(results)
    variabilities.to_csv('variabilities.csv')
    new_df = pd.read_csv('variabilities.csv')
    print(new_df)
