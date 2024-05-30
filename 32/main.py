import psycopg2
from psycopg2 import OperationalError
from tabulate import tabulate
from openpyxl import Workbook
import random

def connect_to_db():
    try:
        conn = psycopg2.connect(
            host='127.0.0.1',
            port=5432,
            dbname='postgres',
            user='postgres',
            password='123456'
        )
        return conn
    except OperationalError as e:
        print(e)

def add(cursor, connection):
    cursor.execute('SELECT * FROM flowers')
    response = cursor.fetchall()

    id = int(input('Enter the flower ID you want to add to the cart: '))
    while True:
        quantity = int(input('Enter the quantity: '))
        if quantity <= response[id-1][3]:
            cursor.execute(f"UPDATE flowers SET stock = stock - {quantity} WHERE id = {id}")
            connection.commit()
            break
        else:
            print("Insufficient stock, please try again.")

    query = f"INSERT INTO cart (name, price, quantity) VALUES ('{response[id-1][1]}', {response[id-1][2]}, {quantity})"
    cursor.execute(query)
    connection.commit()

def delete(cursor, connection):
    id = int(input('Enter the flower ID to delete from the cart: '))
    cursor.execute(f'DELETE FROM cart WHERE id={id}')
    connection.commit()

def show_table(cursor):
    cursor.execute('SELECT * FROM flowers')
    response = cursor.fetchall()
    table = [[row[0], row[1], row[2], row[3]] for row in response]
    print(tabulate(table, headers=['ID', 'Name', 'Price', 'Stock'], tablefmt='pretty'))

def check(cursor):
    wb = Workbook()
    ws = wb.active

    cursor.execute('SELECT * FROM cart')
    response = cursor.fetchall()

    ws.append(["ID", "Name", "Price", "Quantity"])
    total_price = 0

    for row in response:
        ws.append(row)
        total_price += row[2] * row[3]

    ws.append(["", "", "Total price", total_price])

    wb.save("receipt.xlsx")
    print("Receipt saved to receipt.xlsx")

def main():
    connection = connect_to_db()
    cursor = connection.cursor()

    while True:
        print("Welcome to our flower shop. Please select an action:")
        task = int(input('1) Add to Cart\n2) View Flower Catalog\n3) Remove from Cart\n4) Checkout\n: '))
        if 1 <= task <= 4:
            break

    if task == 1:
        add(cursor, connection)
    elif task == 2:
        show_table(cursor)
    elif task == 3:
        delete(cursor, connection)
    elif task == 4:
        check(cursor)

    cursor.close()
    connection.close()

if __name__ == "__main__":
    main()

'''
# Банк из 29 домашки, она не в счет здесб, просто в одном проекте делал
CREATE TABLE bank (
    ID SERIAL PRIMARY KEY,
    card_number CHAR(10) NOT NULL,
    onwer VARCHAR(100) NOT NULL,
    balance INT NOT NULL
);	
	
CREATE TABLE flowers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    stock INT NOT NULL
);

CREATE TABLE cart (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    quantity INTEGER NOT NULL
);

# Chat GPT :)
INSERT INTO flowers (name, price, stock) VALUES
('Роза', 12.99, 50),
('Тюльпан', 8.99, 100),
('Лилия', 15.99, 30),
('Гербера', 7.99, 80),
('Орхидея', 19.99, 20),
('Пион', 11.99, 40),
('Хризантема', 6.99, 60),
('Астра', 9.99, 70),
('Ирис', 10.99, 45),
('Гвоздика', 5.99, 90);

INSERT INTO cart (name, price, quantity) VALUES
('Роза', 12.99, 2),
('Лилия', 15.99, 1),
('Гербера', 7.99, 5),
('Тюльпан', 8.99, 1),
('Ирис', 10.99, 3);
'''