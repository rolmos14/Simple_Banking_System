import random
import sqlite3


class Bank:

    def __init__(self):
        """The constructor to initialize the object."""
        # Connect to database (and create it if it doesn't exists yet)
        self.cards_db_conn = sqlite3.connect("card.s3db")
        # Database cursor
        self.cards_db_cur = self.cards_db_conn.cursor()

        # Create table card if it doesn't exists yet
        self.cards_db_cur.execute("CREATE TABLE IF NOT EXISTS card "
                                  "(id INTEGER, number TEXT, pin TEXT, balance INTEGER DEFAULT 0);")
        self.cards_db_conn.commit()

    def new_account(self):
        # Create data of new account
        # ID must be incremental taking into account last created account
        id = 1  # for first created account
        self.cards_db_cur.execute("SELECT id FROM card")
        accounts = self.cards_db_cur.fetchall()
        if len(accounts) > 0:
            id = accounts[-1][0] + 1  # last account id + 1
        number = str(4 * 10 ** 14 + random.randint(0, 999999999))
        number += self.checksum(number)
        pin = str(random.randint(0, 9999)).rjust(4, '0')
        balance = 0

        # Add new account to DB
        self.cards_db_cur.execute(f"INSERT INTO card VALUES ({id}, {number}, {pin}, {balance});")
        self.cards_db_conn.commit()

        # Print data of new account
        print("\nYour card has been created")
        print(f"Your card number:\n{number}")
        print(f"Your card PIN:\n{pin}\n")

    def close_account(self, account_data):
        # Delete account from DB
        self.cards_db_cur.execute(f"DELETE FROM card WHERE id = {account_data[0]};")
        self.cards_db_conn.commit()
        print(f"\nThe account has been closed!\n")

    @staticmethod
    def checksum(number):
        """Returns checksum digit using Luhn algorithm"""
        total_sum = 0
        for i in range(len(number)):
            n = int(number[i])
            if i % 2 == 0:
                n *= 2
            if n > 9:
                n -= 9
            total_sum += n
        checksum = total_sum % 10
        if checksum > 0:
            checksum = 10 - checksum
        return str(checksum)

    def add_income(self, account_data):
        print("\nEnter income:")
        income = int(input())
        # Update account balance in DB
        self.cards_db_cur.execute(f"UPDATE card SET balance = balance + {income} WHERE id = {account_data[0]};")
        self.cards_db_conn.commit()
        print("Income was added!\n")

    def transfer(self, account_data):
        print("\nTransfer\n"
              "Enter card number:")
        target_number = input()
        # Verify card number valid
        if self.checksum(target_number[0:-1]) == target_number[-1]:
            # Check if target card exists
            self.cards_db_cur.execute(f"SELECT * FROM card WHERE number = {target_number}")
            target_account_data = self.cards_db_cur.fetchone()
            if target_account_data is not None:
                print("Enter how much money you want to transfer:")
                amount = int(input())
                # Check if enough balance
                if amount <= account_data[3]:
                    # Update origin account balance in DB
                    self.cards_db_cur.execute(
                        f"UPDATE card SET balance = balance - {amount} WHERE id = {account_data[0]};")
                    # Update target account balance in DB
                    self.cards_db_cur.execute(
                        f"UPDATE card SET balance = balance + {amount} WHERE id = {target_account_data[0]};")
                    self.cards_db_conn.commit()
                    print("Success!\n")
                else:
                    print("Not enough money!\n")
            else:
                print("Such a card does not exist.\n")
        else:
            print("Probably you made a mistake in the card number. Please try again!\n")

    def login_successful(self, account_data):
        print('\nYou have successfully logged in!\n')
        finish = False  # variable to return True if direct Exit selected
        while True:
            # Update account data from DB to ensure is up to date
            self.cards_db_cur.execute(f"SELECT * FROM card WHERE id = {account_data[0]}")
            account_data = self.cards_db_cur.fetchone()
            print("1. Balance\n"
                  "2. Add income\n"
                  "3. Do transfer\n"
                  "4. Close account\n"
                  "5. Log out\n"
                  "0. Exit")
            option = int(input())
            if option == 1:
                print(f"\nBalance: {account_data[3]}\n")
            elif option == 2:
                self.add_income(account_data)
            elif option == 3:
                self.transfer(account_data)
            elif option == 4:
                self.close_account(account_data)
                break  # force logoff after closing account
            elif option == 5:
                print('\nYou have successfully logged out!\n')
                break
            else:  # option == 0
                finish = True
                break
        return finish

    def login_request(self):
        card_number = input("\nEnter your card number:\n")
        card_pin = input("Enter your PIN:\n")

        # Search for existing account-PIN in DB
        self.cards_db_cur.execute(f"SELECT * FROM card WHERE number = {card_number} AND pin = {card_pin};")
        account_data = self.cards_db_cur.fetchone()

        finish = False  # variable to return True if direct Exit selected
        if account_data is not None:
            finish = self.login_successful(account_data)
        # If account doesn't exist
        else:
            print("\nWrong card number or PIN!\n")
        return finish

    def menu(self):
        while True:
            print("1. Create an account\n"
                  "2. Log into account\n"
                  "0. Exit")
            option = int(input())
            if option == 1:
                self.new_account()
            elif option == 2:
                finish = self.login_request()
                if finish:
                    break
            else:  # option == 0
                break
        # Close connection to DB
        self.cards_db_conn.close()
        print("\nBye!")


bank = Bank()
bank.menu()
