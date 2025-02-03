import requests
from datetime import datetime
from dotenv import load_dotenv, set_key
import os

# Завантажуємо змінні з .env
load_dotenv()

# Файл, у який будемо записувати дані
ENV_FILE = ".env"

# Функція для отримання курсів валют від НБУ
def get_exchange_rates():
    url = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json"
    response = requests.get(url)
    data = response.json()
    
    rates = {"UAH": 1.0}  # Гривня базова
    for item in data:
        if item["cc"] in ["USD", "EUR"]:
            rates[item["cc"]] = item["rate"]  # Курс валюти до UAH
    
    return rates

# Отримуємо актуальні курси валют
exchange_rates = get_exchange_rates()

# Зчитуємо баланс і готівку з .env
amounts = {
    "UAH": float(os.getenv("BALANCE_UAH", 0)),  # Баланс у гривнях
    "USD": float(os.getenv("BALANCE_USD", 0)),  # Баланс у доларах
    "EUR": float(os.getenv("BALANCE_EUR", 0)),  # Баланс у євро
}
cash = float(os.getenv("CASH", 0))  # Готівка в гривнях

# Розрахунок загального балансу у гривнях
total_uah = sum(amount * exchange_rates[currency] for currency, amount in amounts.items()) + cash

# Оновлюємо курси валют і загальний баланс у .env
set_key(ENV_FILE, "TOTAL_BALANCE_UAH", str(round(total_uah, 2)))
set_key(ENV_FILE, "RATE_USD", str(exchange_rates["USD"]))
set_key(ENV_FILE, "RATE_EUR", str(exchange_rates["EUR"]))
set_key(ENV_FILE, "UPDATED_AT", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

# Вивід результатів
print("\nАктуальні курси валют:")
for currency, rate in exchange_rates.items():
    print(f"1 {currency} = {rate:.4f} UAH")

print("\nБаланс у кожній валюті:")
for currency, amount in amounts.items():
    print(f"{currency}: {amount:.2f}")

print(f"\nГотівка (UAH): {cash:.2f}")
print(f"\nЗагальний баланс у гривнях: {total_uah:.2f} UAH")

# Виводимо дату і час виконання скрипта
print(f"\nДата та час виконання: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("\nДані оновлено та записано у .env")
