import tweepy
import requests
import os
from datetime import datetime

# GitHub Secrets'tan anahtarları alıyoruz
X_API_KEY = os.getenv("Fa8jjw4cXofIYcliagfled8du")
X_API_SECRET = os.getenv("vwjgH3p9box5t6NbZMvQB9Gj7twCbYkYjPzqHEIQTFg6ZIxFrl")
X_ACCESS_TOKEN = os.getenv("2032531052045242368-Y6CcwK7NsksDhaXRHuf3OWgwOAUNtz")
X_ACCESS_SECRET = os.getenv("fV44bI11pTe839NqPRD3yxRJEw3TZzqMPyBhCWbzYOgBo")
COLLECT_API_KEY = os.getenv("K6hy0pgKu7Zzj6mbW8EiE2qp")

def get_live_data():
    headers = {'authorization': f"apikey {COLLECT_API_KEY}"}
    try:
        # Döviz
        curr_res = requests.get("https://api.collectapi.com/economy/allCurrency", headers=headers).json()
        dolar = next(item['buying'] for item in curr_res['result'] if item['code'] == 'USD')
        euro = next(item['buying'] for item in curr_res['result'] if item['code'] == 'EUR')
        # Altın
        gold_res = requests.get("https://api.collectapi.com/economy/goldPrice", headers=headers).json()
        ga = next(item['buying'] for item in gold_res['result'] if item['name'] == 'Gram Altın')
        gg = next(item['buying'] for item in gold_res['result'] if item['name'] == 'Gümüş')
        # Petrol
        fuel_res = requests.get("https://api.collectapi.com/gasPrice/turkeyGasoline?city=istanbul", headers=headers).json()
        benzin = fuel_res['result'][0]['benzin']
        
        return {"usd": dolar, "eur": euro, "ga": ga, "gg": gg, "petrol": benzin}
    except: return None

# X Bağlantısı
client = tweepy.Client(X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_SECRET)

v = get_live_data()
if v:
    su_an = datetime.now().strftime('%H:%M')
    mesaj = f"📊 SAATLİK FİNANS RAPORU ({su_an})\n\n💵 Dolar: {v['usd']}₺\n💶 Euro: {v['eur']}₺\n🟡 Altın: {v['ga']}₺\n⚪ Gümüş: {v['gg']}₺\n⛽ Petrol(1L): {v['petrol']}₺\n\n#Dolar #Altın #Ekonomi"
    client.create_tweet(text=mesaj)
