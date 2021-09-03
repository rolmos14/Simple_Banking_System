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
        try:
            self.cards_db_cur.execute("CREATE TABLE card "
                                      "(id INTEGER, number TEXT, pin TEXT, balance INTEGER DEFAULT 0);")
            self.cards_db_conn.commit()
        except sqlite3.OperationalError:
            pass

    def new_account(self):
        # Create data of new account
        id = 0  # not necessary yet, it should be incremental taking into account last existing id in DB
        number = str(4 * 10 ** 14 + random.randint(0, 999999999))
        number += self.checksum(number)
        pin = str(random.randint(0, 9999)).rjust(4, '0')

        # Add new account to DB
        self.cards_db_cur.execute(f"INSERT INTO card VALUES ({id}, {number}, {pin}, 0);")
        self.cards_db_conn.commit()

        # Print data of new account
        print("\nYour card has been created")
        print(f"Your card number:\n{number}")
        print(f"Your card PIN:\n{pin}\n")

    def checksum(self, number):
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

    def login_successful(self, account):
        print('\nYou have successfully logged in!\n')
        finish = False  # variable to return True if direct Exit selected
        while True:
            print("1. Balance\n"
                  "2. Log out\n"
                  "0. Exit")
            option = int(input())
            if option == 1:
                print(f"\nBalance: {account.balance}\n")
            elif option == 2:
                print('\nYou have successfully logged out!\n')
                break
            else:
                finish = True
                break
        return finish

    def login_request(self):
        card_number = input("\nEnter your card number:\n")
        card_pin = input("Enter your PIN:\n")

        # Search for existing account in DB
        self.cards_db_cur.execute(f"SELECT number, pin FROM card WHERE number = {card_number} AND pin = {card_pin};")
        ## CONTINUE HERE WITH FETCHONE, IF SOME RESULT THEN IT IS SUCCESFULL LOGIN AND WE CAN SEND BALANCE TO LOGIN_SUCCESSFUL METHOD
        # Search for existing account and verify PIN
        finish = False  # variable to return True if direct Exit selected
        for account in self.accounts:
            if account.card.number == card_number and account.card.pin == card_pin:
                finish = self.login_successful(account)
                break
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
            else:
                break
        # Close connection to DB
        self.cards_db_conn.close()
        print("\nBye!")

bank = Bank()
bank.menu()
