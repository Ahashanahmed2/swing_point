#scripts/swing_point.py
import pandas as pd
from ta.volatility import BollingerBands
import numpy as np
import os
os.makedirs('stocks/csv',exist_ok=True)

def identify_swing_points(df):
    # Bollinger Bands calculate
    bb = BollingerBands(close=df['close'], window=18, window_dev=2, fillna=True)
    df['upper'] = bb.bollinger_hband()
    df['middle'] = bb.bollinger_mavg()
    df['lower'] = bb.bollinger_lband()

    swing_lows = []
    swing_highs = []

    # Loop through data to find swing lows
    for i in range(2, len(df) - 2):
        candle = df.iloc[i]
        prev_candle = df.iloc[i - 1]
        next_candle = df.iloc[i + 1]
        next2_candle = df.iloc[i + 2]

        # Swing Low condition
        if (
            candle['low'] < prev_candle['low'] and
            candle['low'] <= candle['lower'] and
            candle['close'] < candle['middle'] and
            next_candle['close'] > candle['high'] and
            next2_candle['high'] < next2_candle['close']
        ):
            swing_lows.append((df.index[i], candle['symbol'], candle['low'],candle['date'],candle['high'],candle['open'],candle['close'],next2_candle['close']))
        #__SH condition__
        if(  candle['high'] > prev_candle['high'] and
             candle['close'] > candle['middle'] and
             next_candle['close'] < candle['low'] and 
             next2_candle['close'] < next_candle['close']):
             swing_highs.append((df.index[i],df.index[i+2]))

        #print(f"next2{next2_candle}index:{df.index[i+2]}")
    # Optional: Print or save results
    #print(f"Swing Lows: {swing_lows} /n Swing High:{swing_highs}")

    # Save full DataFrame with BB to CSV
   # df.to_csv(f"stocks/csv/{df['symbol'].mode()[0]}.csv", index=False)

    return swing_lows, swing_highs