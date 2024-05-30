import psycopg2
from psycopg2 import OperationalError

def connect_to_db():
    try:
        conn = psycopg2.connect(host='127.0.0.1', port=5432, dbname='postgres', user='postgres', password='123456')
        return conn
    except OperationalError as e:
        print(e)

connection = connect_to_db()

def create():
    card_num= int(input('Введи номер карты (10 цифр): '))
    name= input('Введи имя: ')
    balance= int(input('Введи баланс карты: '))

    cursor = connection.cursor()
    query = f"INSERT INTO bank (card_number, onwer, balance) VALUES ('{card_num}', '{name}', {balance})"
    cursor.execute(query)
    connection.commit()

def delete():
    id= int(input('Введи id: '))

    cursor = connection.cursor()
    query = f'delete from bank where id={id}'
    cursor.execute(query)
    connection.commit()

def update():
    task= input('Ты будешь менять номер карты(1), имя(2), или баланс карты(3)?: ')
    id= int(input('Введи id: '))
    query = 'update bank set '
    cursor = connection.cursor()

    if task == '1':
        new_card_num = input("Новый номер карты: ")
        query = query + f"card_number='{new_card_num}' "

    if task == '2':
        new_name = input("Новое имя: ")
        query = query + f"onwer='{new_name}' "

    if task == '3':
        new_balance = int(input("Новый баланс: "))
        query = query + f"balance={new_balance} "

    query = query + f' where id={id}'
    cursor.execute(query)
    connection.commit()


def read():
    cursor =connection.cursor()
    querystart = f'select * from bank'
    cursor.execute(querystart)
    response = cursor.fetchall()
    for row in response:
        print(row)

while True:
    task = int(input('Что ты хочешь; Добавить(1), Удалить(2), Изменить(3)?, Посмотреть(4), Выход(5)'))

    if task == 1:
        create()
    elif task == 2:
        delete()

    elif task == 3:
        update()

    elif task == 4:
        read()
    else:
        break