#scripts/mongodb.py
from pymongo import MongoClient
import pandas as pd
from swing_point import identify_swing_points
import os
import subprocess
from dotenv import load_dotenv
load_dotenv()
from collections import defaultdict
swing_high_candles = defaultdict(list)
swing_high_confirms = defaultdict(list)

os.makedirs('./swing/swing_low',exist_ok=True)
os.makedirs('./swing/swing_high/candle/',exist_ok=True)
os.makedirs('./swing/swing_high/buy/',exist_ok=True)
# MongoDB-এ সংযোগ
mongourl = os.getenv("MONGO_URL")
client = MongoClient(mongourl)
db = client["candleData"]
collection = db["candledatas"]


# সবগুলো ডকুমেন্ট নেওয়া (_id ছাড়া)
data = list(collection.find({}, {'_id': 0}))
df = pd.DataFrame(data)

# symbol অনুযায়ী group করা
grouped = df.groupby('symbol')

# প্রতিটি কোম্পানির জন্য identify_swing_points() কল করা
for symbol, group_df in grouped:
   
    swing_lows, swing_highs=  identify_swing_points(group_df)

        # Optional: প্রিন্ট করা  

       
    # for i,symbol,low,date,high,open,close,next2close in swing_lows:
    #     print(f"swing lows:{symbol} date:{date} close:{close} next2close:{next2close} index:{i} \n")
    #     df.to_csv('swing/swing_low/{symbol}.csv')

   
    if len(swing_highs)>0:
     for index_rows_,index_rows__ in swing_highs:
        swing_highs_candle_data=group_df.loc[index_rows_]
        swing_highs_confirm_data=group_df.loc[index_rows__]

       

            # প্রতিটি symbol এর জন্য লিস্টে অ্যাড করা
        swing_high_candles[symbol].append(swing_highs_candle_data)
        swing_high_confirms[symbol].append(swing_highs_confirm_data)
        print(f"swing_high_candles:{swing_high_candles}")

        # আলাদা CSV বানানো
for symbol in swing_high_candles:
    pd.DataFrame(swing_high_candles[symbol]).to_csv(f'./swing/swing_high/candle/{symbol}.csv', index=False)
    pd.DataFrame(swing_high_confirms[symbol]).to_csv(f'./swing/swing_high/buy/{symbol}.csv', index=False)

 
    #print(f"{symbol} - Swing Lows: {swing_lows}")
    #print(f"{symbol} - Swing Highs: {swing_highs}")*-
 
print(f"swing_high:{len(grouped)}")
