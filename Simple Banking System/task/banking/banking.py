import random


class Card:

    def __init__(self):
        """The constructor to initialize the object."""
        self.number = str(4 * 10 ** 14 + random.randint(0, 999999999))
        self.number += self.checksum(self.number)
        self.pin = str(random.randint(0, 9999)).rjust(4, '0')

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


class Account:

    def __init__(self):
        """The constructor to initialize the object."""
        self.balance = 0
        self.card = Card()


class Bank:

    def __init__(self):
        """The constructor to initialize the object."""
        self.accounts = []

    def new_account(self):
        account = Account()
        self.accounts.append(account)
        print("\nYour card has been created")
        print(f"Your card number:\n{account.card.number}")
        print(f"Your card PIN:\n{account.card.pin}\n")

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
        print("\nBye!")

bank = Bank()
bank.menu()
