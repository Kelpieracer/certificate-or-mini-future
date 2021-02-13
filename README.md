# certificate-or-mini-future

I was wondering wether holding bull/bear certificates really is not a good idea, and for holding longer periods, mini-futures would be better.

This piece of script calculates profits of most certificate and mini-future target stocks when holding a certain period of time.
It runs all `HOLDING_TIME` amount of days of target stock's adjclose prices for the duration yahoo is publishing the stock data.

Run by
`python variability.py`
in order to get a `variability.csv` file, which you can upload to excel.

`python etp_gain.py` will show you how gains of a single stock will generate, example is `NOKIA.HE` but you can change it.

Naturally you will need to `pip install` the required libraries first, if you don't already have those.
