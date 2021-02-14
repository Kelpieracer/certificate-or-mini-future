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

    # Interest from Nordnet pricelist https://www.nordnet.fi/fi/markkina/nordnet-markets/kulut-ja-palkkiot
    cert_interest_rate = 0.01 if leverage < 5 else (
        0.03 if leverage > 5 else 0.015)
    cert_interest_per_day = (leverage - 1) * cert_interest_rate / 360
    futu_interest_per_day = 0.03 / 360

    # Loop through all the days in the holding period
    for today in range(0, len(df)-1):
        # This is the price change of one day
        raw_gain = pricelist[today+1] / pricelist[today] - 1

        # Calculate certificate gain for the day
        cert_gain_today = raw_gain * leverage
        cert_gain *= 1 + cert_gain_today - cert_interest_per_day

        # Calculate future gain for the day from leverage of current day
        futu_leverage = pricelist[today] / (pricelist[today] - futu_stop_loss)
        futu_gain_today = raw_gain * futu_leverage
        futu_gain *= 1 + futu_gain_today - futu_interest_per_day

    # Both Mini-Future and Certificate will knock, i.e. they will not go below zero
    return max(0, futu_gain), max(0, cert_gain)


if __name__ == '__main__':

    ticker = 'JBSIEA.SW'  # 'ZSILEU.SW'

    df = si.get_data(ticker, start_date='2020-02-13',
                     end_date='2222-01-01').dropna()['adjclose']
    columns = ['futu', 'cert']
    df_out = pd.DataFrame(columns=columns)
    HOLDING_TIME = len(df)-1        # days
    LEVERAGE = 5

    print(df)

    for today in range(0, len(df) - HOLDING_TIME):
        futu_gain, cert_gain = etp_gain(
            df[list(range(today, today + HOLDING_TIME + 1))], LEVERAGE)
        new_df = pd.DataFrame(
            {'futu': futu_gain, 'cert': cert_gain}, index=[today], columns=columns)
        df_out = df_out.append(new_df)
    print(df_out)
    df_out.to_csv(f'{ticker}.csv')
