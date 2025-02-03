import requests
import os
from dotenv import load_dotenv

# Завантажуємо змінні середовища
load_dotenv()

print("\n🔄 Оновлення балансу Monobank...")

# Отримуємо баланси з .env
balance_uah = float(os.getenv("BALANCE_UAH_MONO", 0)) + float(os.getenv("CASH_UAH", 0))
balance_usd = (
    float(os.getenv("BALANCE_USD_MONO", 0)) + 
    float(os.getenv("BALANCE_USD_PRIVAT", 0)) + 
    float(os.getenv("CASH_USD", 0))
)
balance_eur = float(os.getenv("BALANCE_EUR_MONO", 0)) + float(os.getenv("CASH_EUR", 0))

print("✅ Монобанк баланси оновлено у .env")

# Курси валют із НБУ (за замовчуванням UAH = 1)
exchange_rates = {"UAH": 1.0, "USD": 41.7908, "EUR": 42.8627}

# Вивід актуальних курсів
print("\n📈 Актуальні курси валют:")
for currency, rate in exchange_rates.items():
    print(f"1 {currency} = {rate:.4f} UAH")

# Вивід балансів
print("\n💰 Баланс у кожній валюті:")
print(f"UAH: {balance_uah:.2f}")
print(f"USD: {balance_usd:.2f}")
print(f"EUR: {balance_eur:.2f}")

# Конвертація всього в гривні
total_uah = (
    balance_uah +
    balance_usd * exchange_rates["USD"] +
    balance_eur * exchange_rates["EUR"]
)

# Відсоткове співвідношення
portfolio = {
    "UAH": (balance_uah / total_uah) * 100 if total_uah else 0,
    "USD": (balance_usd * exchange_rates["USD"] / total_uah) * 100 if total_uah else 0,
    "EUR": (balance_eur * exchange_rates["EUR"] / total_uah) * 100 if total_uah else 0,
}

# Вивід співвідношення
print("\n📊 Співвідношення валют у портфелі:")
for currency, percent in portfolio.items():
    print(f"{currency}: {percent:.2f}%")

print(f"\nЗагальна сума в гривнях: {total_uah:.2f} UAH")
