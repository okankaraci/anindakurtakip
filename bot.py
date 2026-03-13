import tweepy
import requests
import os
from datetime import datetime

print("--- BOT CALISMAYA BASLADI ---")

def get_env(name):
    return os.getenv(name)

X_API_KEY = get_env("X_API_KEY")
X_API_SECRET = get_env("X_API_SECRET")
X_ACCESS_TOKEN = get_env("X_ACCESS_TOKEN")
X_ACCESS_SECRET = get_env("X_ACCESS_SECRET")
COL_KEY = get_env("COLLECT_API_KEY")

def get_live_data():
    if not COL_KEY: return None
    auth_key = f"apikey {COL_KEY.replace('apikey ', '')}"
    headers = {'content-type': "application/json", 'authorization': auth_key}
    
    try:
        # Döviz
        curr_res = requests.get("https://api.collectapi.com/economy/allCurrency", headers=headers).json()
        if 'result' not in curr_res:
            print("HATA: Doviz verisi 'result' icermiyor. Aboneliginizi kontrol edin.")
            return None
            
        dolar = next(item['buying'] for item in curr_res['result'] if item['code'] == 'USD')
        euro = next(item['buying'] for item in curr_res['result'] if item['code'] == 'EUR')
        
        # Altın
        gold_res = requests.get("https://api.collectapi.com/economy/goldPrice", headers=headers).json()
        ga = next(item['buying'] for item in gold_res['result'] if item['name'] == 'Gram Altın')
        
        # Akaryakıt
        fuel_res = requests.get("https://api.collectapi.com/gasPrice/turkeyGasoline?city=istanbul", headers=headers).json()
        benzin = fuel_res['result'][0]['benzin']
        
        return {"usd": dolar, "eur": euro, "ga": ga, "petrol": benzin}
    except Exception as e:
        print(f"Veri hatasi ayrintisi: {e}")
        return None

try:

    client = tweepy.Client(
        consumer_key=X_API_KEY, 
        consumer_secret=X_API_SECRET,
        access_token=X_ACCESS_TOKEN, 
        access_token_secret=X_ACCESS_SECRET)
    
    v = get_live_data()
    if v:
        su_an = datetime.now().strftime('%H:%M')
        mesaj = f"📊 SAATLİK VERİ ({su_an})\n\n💵 Dolar: {v['usd']}₺\n💶 Euro: {v['eur']}₺\n🟡 Altın: {v['ga']}₺\n⛽ Petrol: {v['petrol']}₺"
        
        client.create_tweet(text=mesaj, user_auth=True) 
        print("--- TWEET BASARIYLA ATILDI ---")
    else:
        print("Veri hatası.")
except Exception as e:
    print(f"X Hatası: {e}")
