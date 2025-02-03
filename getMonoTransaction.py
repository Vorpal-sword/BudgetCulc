import requests
import os
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Завантаження змінних з .env
load_dotenv()

# Отримання токену Monobank з .env
MONO_API_TOKEN = os.getenv("MONO_API_TOKEN")
if not MONO_API_TOKEN:
    print("Помилка: встановіть MONO_API_TOKEN у .env")
    exit(1)

headers = {"X-Token": MONO_API_TOKEN}

# Отримання інформації про клієнта (список карток)
client_info_url = "https://api.monobank.ua/personal/client-info"
response = requests.get(client_info_url, headers=headers)
if response.status_code != 200:
    print("Помилка отримання даних клієнта:", response.text)
    exit(1)

client_info = response.json()
accounts = client_info.get("accounts", [])
if not accounts:
    print("Не знайдено жодної картки")
    exit(1)

# Вивід списку карток з індексами
print("Список карток:")
for idx, account in enumerate(accounts):
    masked_pan = account.get("maskedPan", ["Невідома картка"])
    currency_code = account.get("currencyCode")
    print(f"{idx + 1}. {masked_pan} (Код валюти: {currency_code})")

# Запит користувача, яку картку обрати
while True:
    try:
        choice = int(input("\nВведіть номер картки, для якої потрібно отримати виписку: "))
        if 1 <= choice <= len(accounts):
            break
        else:
            print("Невірний номер картки. Спробуйте ще раз.")
    except ValueError:
        print("Будь ласка, введіть числове значення.")

selected_account = accounts[choice - 1]
account_id = selected_account.get("id")
masked_pan = selected_account.get("maskedPan", ["Невідома картка"])
currency_code = selected_account.get("currencyCode")

# Визначаємо часовий діапазон для виписки (наприклад, останні 7 днів)
end_date = datetime.now()
start_date = end_date - timedelta(days=7)
start_ts = int(start_date.timestamp() * 1000)  # перетворення у мілісекунди
end_ts = int(end_date.timestamp() * 1000)

print(f"\nОтримання транзакцій для картки {masked_pan} (Код валюти: {currency_code})")
print(f"Період: з {start_date} до {end_date}\n")

# Формуємо URL запиту транзакцій
transactions_url = f"https://api.monobank.ua/personal/statement/{account_id}/{start_ts}/{end_ts}"

# Виконуємо запит
tx_response = requests.get(transactions_url, headers=headers)

if tx_response.status_code != 200:
    print("Помилка отримання транзакцій:", tx_response.text)
else:
    transactions = tx_response.json()
    if not transactions:
        print("За вибраний період транзакцій не знайдено.")
    else:
        print("Транзакції:")
        for tx in transactions:
            # Час транзакції (Unix timestamp у секундах)
            tx_time = datetime.fromtimestamp(tx.get("time", 0))
            # Сума (баланс у копійках, перетворюємо у звичний формат)
            amount = tx.get("amount", 0) / 100
            description = tx.get("description", "Без опису")
            print(f"  {tx_time} | {description} | Сума: {amount}")

# Затримка для уникнення перевищення ліміту запитів (необов'язково)
time.sleep(1)
