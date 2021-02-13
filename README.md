# Certificate or Mini-Future

Kepieracer, 2021-02-13

License: Use as you want, but don't blame me.

This is not an investment advice.

## Why

I was wondering wether holding bull/bear certificates really is not a good idea, and for holding longer periods, mini-futures would be better.

This piece of script calculates profits of most certificate and mini-future target stocks when holding a certain period of time.
It runs all `HOLDING_TIME` amount of days of target stock's `adjclose` prices for the duration which Yahoo is publishing the stock data.

## How to run

From command line, run

`python variability.py`

in order to get a `variability.csv` file, which you can upload to excel.

Naturally you will need to `pip install` the required libraries first, if you don't already have those.

## Follow a single stock item, for example to check if calculation is correct

`python etp_gain.py`

will show you how gains of a single stock will generate, example is `NOKIA.HE` but you can change it.

## Finally

If you find any issues with this, or that it is even completely wrong, or maybe you find this interesting or are developing it further, I'd be happy to hear about it!
