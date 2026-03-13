import tweepy
import requests
import os
from datetime import datetime

print("--- BOT CALISMAYA BASLADI ---")

# Anahtarları çek ve kontrol et
def get_env(name):
    val = os.getenv(name)
    if not val:
        print(f"DIKKAT: {name} GitHub Secrets icinde bulunamadi!")
    return val

X_API_KEY = get_env("X_API_KEY")
X_API_SECRET = get_env("X_API_SECRET")
X_ACCESS_TOKEN = get_env("X_ACCESS_TOKEN")
X_ACCESS_SECRET = get_env("X_ACCESS_SECRET")
COL_KEY = get_env("COLLECT_API_KEY")

def get_live_data():
    if not COL_KEY: return None
    
    # Hata veren kısım düzeltildi
    auth_key = f"apikey {COL_KEY.replace('apikey ', '')}"
    headers = {'content-type': "application/json", 'authorization': auth_key}
    
    try:
        # Döviz
        curr_res = requests.get("https://api.collectapi.com/economy/allCurrency", headers=headers).json()
        dolar = next(item['buying'] for item in curr_res['result'] if item['code'] == 'USD')
        euro = next(item['buying'] for item in curr_res['result'] if item['code'] == 'EUR')
        
        # Altın
        gold_res = requests.get("https://api.collectapi.com/economy/goldPrice", headers=headers).json()
        ga = next(item['buying'] for item in gold_res['result'] if item['name'] == 'Gram Altın')
        try:
            gg = next(item['buying'] for item in gold_res['result'] if 'Gümüş' in item['name'])
        except:
            gg = "N/A"
        
        # Akaryakıt
        fuel_res = requests.get("https://api.collectapi.com/gasPrice/turkeyGasoline?city=istanbul", headers=headers).json()
        benzin = fuel_res['result'][0]['benzin']
        
        return {"usd": dolar, "eur": euro, "ga": ga, "gg": gg, "petrol": benzin}
    except Exception as e:
        print(f"Veri hatasi olustu: {e}")
        return None

try:
    if all([X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_SECRET, COL_KEY]):
        client = tweepy.Client(X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_SECRET)
        v = get_live_data()
        
        if v:
            su_an = datetime.now().strftime('%H:%M')
            mesaj = (f"📊 SAATLİK FİNANS RAPORU ({su_an})\n\n"
                     f"💵 Dolar: {v['usd']}₺\n"
                     f"💶 Euro: {v['eur']}₺\n"
                     f"🟡 Altın: {v['ga']}₺\n"
                     f"⚪ Gümüş: {v['gg']}₺\n"
                     f"⛽ Petrol(1L): {v['petrol']}₺\n\n"
                     f"#Dolar #Altın #Ekonomi")
            
            client.create_tweet(text=mesaj)
            print("--- TWEET BASARIYLA ATILDI ---")
        else:
            print("Veri hatası nedeniyle tweet atılmadı.")
    else:
        print("Eksik anahtarlar var, lutfen GitHub Secrets'i kontrol edin.")
except Exception as e:
    print(f"KRITIK HATA: {e}")
