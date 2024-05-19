import sys

account = {'full_name': '', 'age': 0, 'password': '', 'balance': 0, 'treshold': 0, 'transactions': []}

def log_error_and_exit(err_msg):
    print(f"ERROR: {err_msg}")
    sys.exit(1)

def create_account():
    account['full_name'] = input("Введите Ф.И.О: ")
    birth_year = input("Введите год рождения: ")
    if not birth_year.isdigit():
        log_error_and_exit("Год рождения должен быть числом.")
    account['age'] = 2024 - int(birth_year)
    account['password'] = input("Введите пароль: ")
    print(f"Создан аккаунт: {account['full_name']} {account['age']}")
    print("Аккаунт успешно зарегистрирован!")

def deposit_money():
    amount = input("Введите сумму пополнения: ")
    try:
        amount = float(amount)
        if amount <= 0:
            log_error_and_exit("Сумма должна быть больше нуля.")
        account['balance'] += amount
        print("Счёт успешно пополнен на сумму:", amount)
    except ValueError:
        log_error_and_exit("Неверный формат суммы, должно быть число.")

def withdraw_money():
    check = input("Введите пароль: ")
    if check != account['password']:
        log_error_and_exit("Неверный пароль!")
    amount = input("Введите сумму для снятия: ")
    try:
        amount = float(amount)
        if amount > account['balance']:
            log_error_and_exit("Недостаточно средств на счету.")
        elif amount <= 0:
            log_error_and_exit("Сумма должна быть больше нуля.")
        account['balance'] -= amount
        print(f"Вы сняли {amount} с вашего счета.")
    except ValueError:
        log_error_and_exit("Ошибка при вводе суммы.")

def handle_transaction():
    comment = input("Введите комментарий для транзакции: ")
    amount = input("Введите сумму: ")
    try:
        amount = float(amount)
        transaction = {'comment': comment, 'amount': amount}
        account['transactions'].append(transaction)
        print(f"Транзакция добавлена. Комментарий: {comment}, сумма: {amount}")
    except ValueError:
        log_error_and_exit("Ошибка при вводе данных транзакции.")

def set_treshold():
    treshold = input("Введите новый лимит транзакций: ")
    try:
        treshold = float(treshold)
        account['treshold'] = treshold
        print(f"Лимит транзакций установлен на: {treshold}")
    except ValueError:
        log_error_and_exit("Ошибка при установке лимита. Введите число.")

def apply_transactions():
    new_transactions = []
    for transaction in account['transactions']:
        if transaction['amount'] <= account['treshold']:
            account['balance'] += transaction['amount']
            print(f"Транзакция на {transaction['amount']} применена.")
        else:
            new_transactions.append(transaction)
            print(f"Транзакция на {transaction['amount']} отклонена из-за лимита.")
    account['transactions'] = new_transactions

def show_transaction_stats():
    freq = {}
    for transaction in account['transactions']:
        amount = transaction['amount']
        if amount in freq:
            freq[amount] += 1
        else:
            freq[amount] = 1
    for amount, count in freq.items():
        print(f"Транзакций с суммой {amount}: {count}")

def filter_by_amount():
    filter_amount = input("Введите сумму для фильтрации: ")
    try:
        filter_amount = float(filter_amount)
        for transaction in account['transactions']:
            if transaction['amount'] >= filter_amount:
                yield transaction
    except ValueError:
        log_error_and_exit("Неверный формат суммы, должно быть число.")

def show_filtered_transactions():
    print("Фильтрация транзакций по заданной сумме:")
    filtered_transactions = filter_by_amount()
    for transaction in filtered_transactions:
        print(f"Транзакция: Комментарий - {transaction['comment']}, Сумма - {transaction['amount']}")

def save_to_file():
    try:
        with open("account_data.txt", "w") as file_out:
            file_out.write(f"{account['full_name']}\n")
            file_out.write(f"{account['age']}\n")
            file_out.write(f"{account['password']}\n")
            file_out.write(f"{account['balance']}\n")
            file_out.write(f"{account['treshold']}\n")
            for transaction in account['transactions']:
                file_out.write(f"{transaction['comment']}:{transaction['amount']}\n")
        print("Данные аккаунта сохранены.")
    except Exception as e:
        print(f"Ошибка при сохранении данных: {e}")

def load_from_file():
    try:
        with open("account_data.txt", "r") as file_in:
            account['full_name'] = file_in.readline().strip()
            account['age'] = int(file_in.readline().strip())
            account['password'] = file_in.readline().strip()
            account['balance'] = float(file_in.readline().strip())
            account['treshold'] = float(file_in.readline().strip())
            account['transactions'] = []
            for line in file_in:
                comment, amount = line.strip().split(':')
                account['transactions'].append({'comment': comment, 'amount': float(amount)})
        print("Данные аккаунта загружены.")
    except FileNotFoundError:
        print("Файл данных не найден. Создайте новый аккаунт.")
    except Exception as e:
        print(f"Ошибка при загрузке данных: {e}")

def main():
    print("Загрузить ваши данные?" + "\n" + "1. Да" + "\n" + "2. Нет")
    choice = input("Выберите вариант: ")
    if choice == "1":
        load_from_file()
    elif choice == "2":
        print("Начните с создания нового аккаунта.")

    while True:
        print("\nДоступные операции:")
        print("1. Создать аккаунт")
        print("2. Положить деньги на счёт")
        print("3. Снять деньги со счёта")
        print("4. Вывести баланс на экран")
        print("5. Создать транзакцию")
        print("6. Установить лимит")
        print("7. Применить транзакции")
        print("8. Статистика транзакций")
        print("9. Фильтр транзакций по сумме")
        print("10. Выйти из программы")

        cmd = input("Выберите номер операции: ")
        if not cmd.isdigit():
            log_error_and_exit("Номер операции должен быть числом.")
        cmd = int(cmd)
        if cmd == 1:
            create_account()
        elif cmd == 2:
            deposit_money()
        elif cmd == 3:
            withdraw_money()
        elif cmd == 4:
            print("Ваш текущий баланс: ", account['balance'])
        elif cmd == 5:
            handle_transaction()
        elif cmd == 6:
            set_treshold()
        elif cmd == 7:
            apply_transactions()
        elif cmd == 8:
            show_transaction_stats()
        elif cmd == 9:
            show_filtered_transactions()
        elif cmd == 10:
            print("Выход из программы...")
            break
        else:
            log_error_and_exit("Неверный номер операции или аккаунт не создан.")
        save_to_file()

if __name__ == "__main__":
    main()
