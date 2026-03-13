import tweepy
import requests
import os
from datetime import datetime

print("--- BOT CALISMAYA BASLADI ---")

# GitHub Secrets'tan anahtarları al
X_API_KEY = os.getenv("Fa8jjw4cXofIYcliagfled8du")
X_API_SECRET = os.getenv("vwjgH3p9box5t6NbZMvQB9Gj7twCbYkYjPzqHEIQTFg6ZIxFrl")
X_ACCESS_TOKEN = os.getenv("2032531052045242368-Y6CcwK7NsksDhaXRHuf3OWgwOAUNtz")
X_ACCESS_SECRET = os.getenv("fV44bI11pTe839NqPRD3yxRJEw3TZzqMPyBhCWbzYOgBo")
COLLECT_API_KEY = os.getenv("jK6hy0pgKu7Zzj6mbW8EiE2qp")

def get_live_data():
    print("Veriler cekiliyor...")
    headers = {'authorization': f"apikey {COLLECT_API_KEY}"}
    try:
        res = requests.get("https://api.collectapi.com/economy/allCurrency", headers=headers)
        if res.status_code != 200:
            print(f"Hata: API {res.status_code} dondu.")
            return None
        
        data = res.json()
        dolar = next(item['buying'] for item in data['result'] if item['code'] == 'USD')
        euro = next(item['buying'] for item in data['result'] if item['code'] == 'EUR')
        
        gold_res = requests.get("https://api.collectapi.com/economy/goldPrice", headers=headers).json()
        ga = next(item['buying'] for item in gold_res['result'] if item['name'] == 'Gram Altın')
        gg = next(item['buying'] for item in gold_res['result'] if item['name'] == 'Gümüş')
        
        fuel_res = requests.get("https://api.collectapi.com/gasPrice/turkeyGasoline?city=istanbul", headers=headers).json()
        benzin = fuel_res['result'][0]['benzin']
        
        return {"usd": dolar, "eur": euro, "ga": ga, "gg": gg, "petrol": benzin}
    except Exception as e:
        print(f"Veri hatasi: {e}")
        return None

try:
    client = tweepy.Client(X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_SECRET)
    v = get_live_data()
    
    if v:
        su_an = datetime.now().strftime('%H:%M')
        mesaj = f"📊 SAATLİK FİNANS RAPORU ({su_an})\n\n💵 Dolar: {v['usd']}₺\n💶 Euro: {v['eur']}₺\n🟡 Altın: {v['ga']}₺\n⚪ Gümüş: {v['gg']}₺\n⛽ Petrol(1L): {v['petrol']}₺\n\n#Dolar #Altın #Ekonomi"
        
        print(f"Tweet gonderiliyor: {mesaj}")
        client.create_tweet(text=mesaj)
        print("--- TWEET BASARIYLA ATILDI ---")
    else:
        print("Veri bos geldigi icin tweet atilmadi.")
except Exception as e:
    print(f"KRITIK HATA: {e}")
