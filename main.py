import os
import requests
from datetime import datetime
from dotenv import load_dotenv, set_key

# 1. Спочатку оновлюємо баланс Monobank
print("🔄 Оновлення балансу Monobank...")
os.system("python getMonoBalance.py")  # Викликаємо скрипт оновлення

# 2. Завантажуємо змінні з .env після оновлення
load_dotenv()
ENV_FILE = ".env"

# 3. Функція для отримання курсів валют з НБУ
def get_exchange_rates():
    url = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json"
    response = requests.get(url)
    data = response.json()

    rates = {"UAH": 1.0}  # Базовий курс для гривні
    for item in data:
        if item["cc"] in ["USD", "EUR"]:
            rates[item["cc"]] = item["rate"]
    return rates

# 4. Отримуємо курси валют
exchange_rates = get_exchange_rates()

# 5. Зчитуємо баланс з .env
amounts = {
    "UAH": float(os.getenv("CASH_UAH", 0)) + float(os.getenv("BALANCE_UAH_MONO", 0)),
    "USD": float(os.getenv("BALANCE_USD_PRIVAT", 0)) + float(os.getenv("BALANCE_USD_MONO", 0)),
    "EUR": float(os.getenv("CASH_BALANCE_EUR", 0)) + float(os.getenv("BALANCE_EUR_MONO", 0)),
}

# 6. Розраховуємо загальний баланс у гривнях
total_uah = sum(amount * exchange_rates[currency] for currency, amount in amounts.items())

# 7. Оновлюємо .env із загальним балансом
set_key(ENV_FILE, "TOTAL_BALANCE_UAH", str(round(total_uah, 2)))
set_key(ENV_FILE, "UPDATED_AT", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

# 8. Виводимо результати
print("\n📈 Актуальні курси валют:")
for currency, rate in exchange_rates.items():
    print(f"1 {currency} = {rate:.4f} UAH")

print("\n💰 Баланс у кожній валюті:")
for currency, amount in amounts.items():
    print(f"{currency}: {amount:.2f}")

print(f"\n📊 Загальний баланс у гривнях: {total_uah:.2f} UAH")
print(f"\n🕒 Дата та час виконання: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("\n✅ Дані оновлено та записано у .env")
