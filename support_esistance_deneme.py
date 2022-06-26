from candlestick import candlestick
import pandas as pd
import requests
import ccxt, config
exchange = ccxt.binance({
            "apiKey": config.apiKey,
            "secret": config.secretKey,

            'options': {
                'defaultType': 'future'
            },
            'enableRateLimit': True,
            'adjustForTimeDifference': True
        })
# Find candles where inverted hammer is detected
bars = exchange.fetch_ohlcv(symbol="USDTBTC", timeframe="4h", since=None,)
data = pd.DataFrame(bars, columns=['T', 'open', 'high', 'low', 'close', 'V', 'CT', 'QV', 'N', 'TB', 'TQ', 'I'])

data['T'] = pd.to_datetime(data['T'], unit='ms')





target = 'InvertedHammers'
data = candlestick.inverted_hammer(data, target=target)
# candles_df = candlestick.doji_star(candles_df)
# candles_df = candlestick.bearish_harami(candles_df)
# candles_df = candlestick.bullish_harami(candles_df)
# candles_df = candlestick.dark_cloud_cover(candles_df)
# candles_df = candlestick.doji(candles_df)
# candles_df = candlestick.dragonfly_doji(candles_df)
# candles_df = candlestick.hanging_man(candles_df)
# candles_df = candlestick.gravestone_doji(candles_df)
# candles_df = candlestick.bearish_engulfing(candles_df)
# candles_df = candlestick.bullish_engulfing(candles_df)
# candles_df = candlestick.hammer(candles_df)
# candles_df = candlestick.morning_star(candles_df)
# candles_df = candlestick.morning_star_doji(candles_df)
# candles_df = candlestick.piercing_pattern(candles_df)
# candles_df = candlestick.rain_drop(candles_df)
# candles_df = candlestick.rain_drop_doji(candles_df)
# candles_df = candlestick.star(candles_df)
# candles_df = candlestick.shooting_star(candles_df)

print(candles_df[candles_df[target] == True][['T', target]])