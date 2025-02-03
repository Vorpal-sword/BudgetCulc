import requests
import os
from dotenv import load_dotenv, set_key

# Завантажуємо змінні середовища
load_dotenv()
ENV_FILE = ".env"

def getMonoBalance():
    """
    Отримує баланс по всіх картках з Monobank і оновлює .env:
      - BALANCE_UAH_MONO
      - BALANCE_USD_MONO
      - BALANCE_EUR_MONO
    """
    MONO_API_TOKEN = os.getenv("MONO_API_TOKEN")
    if not MONO_API_TOKEN:
        print("Помилка: MONO_API_TOKEN не встановлено у .env")
        return

    headers = {"X-Token": MONO_API_TOKEN}
    client_info_url = "https://api.monobank.ua/personal/client-info"
    response = requests.get(client_info_url, headers=headers)
    
    if response.status_code != 200:
        print("Помилка отримання даних клієнта з Monobank:", response.text)
        return

    data = response.json()

    # Ініціалізуємо баланси для кожної валюти
    balances = {"UAH": 0, "USD": 0, "EUR": 0}

    for account in data.get("accounts", []):
        currency_code = account.get("currencyCode")
        balance = float(account.get("balance", 0)) / 100  # Монобанк повертає баланс у копійках
        if currency_code == 980:  # UAH
            balances["UAH"] += balance
        elif currency_code == 840:  # USD
            balances["USD"] += balance
        elif currency_code == 978:  # EUR
            balances["EUR"] += balance

    # Оновлюємо .env
    set_key(ENV_FILE, "BALANCE_UAH_MONO", f"{balances['UAH']:.2f}")
    set_key(ENV_FILE, "BALANCE_USD_MONO", f"{balances['USD']:.2f}")
    set_key(ENV_FILE, "BALANCE_EUR_MONO", f"{balances['EUR']:.2f}")
    
    print("✅ Монобанк баланси оновлено у .env")

if __name__ == "__main__":
    getMonoBalance()
