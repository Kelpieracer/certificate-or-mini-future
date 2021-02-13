import pandas as pd
from yahoo_fin import stock_info as si


def etp_gain(df, leverage):
    # List is easier to loop
    pricelist = df.tolist()
    # Certificate gains depend on previous value
    cert_gain = 1
    # Future leverage is variable, and it depends on stoploss level
    futu_stop_loss = pricelist[0] * (1 - 1/leverage)
    futu_gain = 1

    # Loop through all the days in the holding period
    for today in range(0, len(df)-1):
        # This is the price change of one day
        raw_gain = pricelist[today+1] / pricelist[today] - 1

        # Calculate certificate gain for the day
        cert_gain_today = raw_gain * leverage
        cert_gain *= 1 + cert_gain_today

        # Calculate future gain for the day from leverage of current day
        futu_leverage = pricelist[today] / (pricelist[today] - futu_stop_loss)
        futu_gain_today = raw_gain * futu_leverage
        futu_gain * 1 + futu_gain_today

    # Both Mini-Future and Certificate will knock, i.e. they will not go below zero
    return max(0, futu_gain), max(0, cert_gain)


if __name__ == '__main__':
    df = pd.DataFrame([1, 1, 1], columns=['adjclose'])
    l = 1
    f, c = etp_gain(df['adjclose'], l)
    print(f'prices {df["adjclose"].tolist()}   lev {l}   futu {f}    cert {c}')

    df = pd.DataFrame([1, 2], columns=['adjclose'])
    f, c = etp_gain(df['adjclose'], l)
    print(f'prices {df["adjclose"].tolist()}   lev {l}   futu {f}    cert {c}')

    df = pd.DataFrame([1, 2, 3], columns=['adjclose'])
    l = 2
    f, c = etp_gain(df['adjclose'], l)
    print(f'prices {df["adjclose"].tolist()}   lev {l}   futu {f}    cert {c}')

    df = pd.DataFrame([1, 2, 3], columns=['adjclose'])
    f, c = etp_gain(df['adjclose'], l)
    print(f'prices {df["adjclose"].tolist()}   lev {l}   futu {f}    cert {c}')

    df = pd.DataFrame([1, 2, 1], columns=['adjclose'])
    l = 1
    f, c = etp_gain(df['adjclose'], l)
    print(f'prices {df["adjclose"].tolist()}   lev {l}   futu {f}    cert {c}')

    df = pd.DataFrame([1, 2, 1], columns=['adjclose'])
    l = 2
    f, c = etp_gain(df['adjclose'], l)
    print(f'prices {df["adjclose"].tolist()}   lev {l}   futu {f}    cert {c}')

    df = pd.DataFrame([1, 2, 4, 5, 6], columns=['adjclose'])
    l = 2
    f, c = etp_gain(df['adjclose'], l)
    print(f'prices {df["adjclose"].tolist()}   lev {l}   futu {f}    cert {c}')

    df = pd.DataFrame([1, 1.1, 1.2, 1.1, 1.3], columns=['adjclose'])
    l = 5
    f, c = etp_gain(df['adjclose'], l)
    print(f'prices {df["adjclose"].tolist()}   lev {l}   futu {f}    cert {c}')

    df = si.get_data('NOKIA.HE', start_date='2010-01-01',
                     end_date='2020-01-01').dropna()['adjclose']
    columns = ['futu', 'cert']
    df_out = pd.DataFrame(columns=columns)
    HOLDING_TIME = 5        # days
    LEVERAGE = 5
    for today in range(0, len(df) - HOLDING_TIME):
        futu_gain, cert_gain = etp_gain(
            df[list(range(today, today + HOLDING_TIME + 1))], LEVERAGE)
        new_df = pd.DataFrame(
            {'futu': futu_gain, 'cert': cert_gain}, index=[today], columns=columns)
        df_out = df_out.append(new_df)
    print(df_out)
    df_out.to_csv('test.csv')
