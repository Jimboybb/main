import os
import random
import time

class SimpleBankingSystem:
    def __init__(self):
        self.accounts = {}
        self.usernames = {}
        self.logged_in_account = None
        self.accounts_file = "accounts.txt"
        self.transactions_folder = "transactions"
        if not os.path.exists(self.transactions_folder):
            os.makedirs(self.transactions_folder)
        self.load_accounts()

    def generate_random_account_number(self):
        while True:
            random_account_number = random.randint(100000, 999999)
            if random_account_number not in self.accounts:
                return random_account_number

    def create_account(self, username, pin, initial_balance):
        while True:
            if self.is_valid_amount(initial_balance):
                initial_balance = float(initial_balance)
                if initial_balance < 100:
                    print("Processing Request to Create an Account...")
                    time.sleep(2)
                    print("Initial balance must be ₱100 or more. Please try again.")
                    initial_balance = input("Enter initial balance: ")
                else:
                    break
            else:
                print("Processing Request to Create an Account...")
                time.sleep(2)
                print("Invalid input. Please enter a numerical value.")
                initial_balance = input("Enter initial balance: ")

        print("\n----Account Details----")
        print("Username: ", username)
        print("Pin: ", pin)
        print("Initial Balance: ", initial_balance)
        print("------------------------")
        answer = input("Do you wish to continue creating your account? (yes/no): ").lower()
        while True:
            if answer in ['yes', 'y']:
                print("Processing Request to Create an Account...")
                time.sleep(2)
                break
            elif answer in ['no', 'n']:
                print("Account creation is void.")
                print("----------------------------------------\n")
                return
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")
                answer = input("Do you wish to continue creating your account? (yes/no): ").lower()

        account_number = self.generate_random_account_number()

        while username in self.usernames:
            print("Username already exists. Please try again.")
            username = self.input_username()
            print("Processing Request to Create an Account...")
            time.sleep(2)

        self.accounts[account_number] = {'Username': username, 'PIN': pin, 'Balance': initial_balance}
        self.usernames[username] = account_number
        self.save_accounts()  # Save the account details to the file
        self.save_transaction_history(account_number, [])
        print(f"Account created successfully. Your account number is: {account_number}\n")

    def log_in(self, account_number, pin):
        if account_number not in self.accounts:
            print("Account number not found. Please try again.")
            return False
        else:
            try:
                entered_pin = int(pin)
                if self.accounts[account_number]['PIN'] == pin:
                    self.logged_in_account = account_number
                    return True
                else:
                    print("Confirming your Identity...")
                    time.sleep(2)
                    print("Incorrect PIN. Please try again.")
                    return False
            except ValueError:
                print("Confirming your Identity...")
                time.sleep(2)
                print("Invalid PIN. Please enter a numeric PIN.")
                return False

    def log_out(self):
        print("Logging Out...")
        time.sleep(2)
        print("Successfully logged out.")
        print("----------------------------------------\n")
        self.logged_in_account = None

    def check_balance(self, account_number):
        print(f"Current Balance for Account {account_number} ({self.accounts[account_number]['Username']}):  ₱{self.accounts[account_number]['Balance']}")

    def deposit(self, account_number, amount):
        if amount < 10:
            print("Minimum deposit amount is ₱10. Please enter a higher amount.")
            return False

        self.accounts[account_number]['Balance'] += amount
        self.add_transaction(account_number, 'deposit', amount)
        self.save_accounts()  # Save the updated balance to the file
        print("Deposit successful.")
        return True

    def withdraw(self, account_number, amount):
        if amount <= 0:
            print("Invalid withdrawal amount. Please enter a positive amount.")
            return False
        elif amount > self.accounts[account_number]['Balance']:
            print("Insufficient funds. Withdrawal canceled.")
            return False

        self.accounts[account_number]['Balance'] -= amount
        self.add_transaction(account_number, 'withdrawal', amount)
        self.save_accounts()  # Save the updated balance to the file
        print("Withdrawal successful.")
        return True

    def show_transaction_history(self, account_number):
        print(f"Transaction History for Account {account_number} ({self.accounts[account_number]['Username']}):")
        transactions = self.load_transaction_history(account_number)
        for transaction in transactions:
            print(transaction)
        print("----------------------------------------\n")

    def input_pin(self):
        while True:
            pin = input("Set your 8-digit PIN: ")
            if len(pin) == 8 and pin.isdigit():
                return pin
            else:
                print("Invalid PIN. Please enter an 8-digit PIN.")

    def input_username(self):
        while True:
            Fname = input("Enter your First Name: ").capitalize()
            if not Fname.isalpha():
                print("Please enter letters only.")
            else:
                Lname = input("Enter your Last Name: ").capitalize()
                if not Lname.isalpha():
                    print("Please enter letters only.")
                else:
                    username = f"{Fname} {Lname}"
                    return username

    def is_valid_amount(self, amount):
        try:
            float(amount)
            return True
        except ValueError:
            return False

    def save_accounts(self):
        with open(self.accounts_file, 'w') as file:
            for account_number, account_details in self.accounts.items():
                line = f"{account_number},{account_details['Username']},{account_details['PIN']},{account_details['Balance']}\n"
                file.write(line)

    def load_accounts(self):
        if os.path.exists(self.accounts_file):
            with open(self.accounts_file, 'r') as file:
                for line in file:
                    account_number, username, pin, balance = line.strip().split(',')
                    account_number = int(account_number)
                    balance = float(balance)
                    self.accounts[account_number] = {'Username': username, 'PIN': pin, 'Balance': balance}
                    self.usernames[username] = account_number

    def save_transaction_history(self, account_number, transactions):
        with open(f"{self.transactions_folder}/{account_number}.txt", 'w') as file:
            for transaction in transactions:
                line = f"{transaction['type']},{transaction['amount']}\n"
                file.write(line)

    def load_transaction_history(self, account_number):
        transactions = []
        try:
            with open(f"{self.transactions_folder}/{account_number}.txt", 'r') as file:
                for line in file:
                    transaction_type, amount = line.strip().split(',')
                    amount = float(amount)
                    transactions.append({'type': transaction_type, 'amount': amount})
        except FileNotFoundError:
            pass
        return transactions

    def add_transaction(self, account_number, transaction_type, amount):
        transactions = self.load_transaction_history(account_number)
        transactions.append({'type': transaction_type, 'amount': amount})
        self.save_transaction_history(account_number, transactions)

bank_system = SimpleBankingSystem()

# Main loop
while True:
    print("----Welcome to GengGeng Bank----")
    print("\nLogin Interface")
    print("1. Create Account")
    print("2. Log In")
    print("3. Exit\n")

    choice = input("Enter your choice: ")

    if choice == '1':
        username = bank_system.input_username()
        pin = bank_system.input_pin()
        initial_balance = input("Enter your initial balance: ")
        bank_system.create_account(username, pin, initial_balance)

    elif choice == '2':
        while True:
            account_number = input("Enter account number: ")
            if account_number.isdigit():
                account_number = int(account_number)
                break
            else:
                print("Invalid input. Account number must be a number.")

        pin = input("Enter PIN: ")
        if bank_system.log_in(account_number, pin):
            print("Logging in...")
            time.sleep(2)
            print("Log-in successful.\n")
            print("----------------------------------------")

            while True:
                print("-----MAIN MENU-----\n")
                bank_system.check_balance(account_number)
                print(" ")

                print("1. Deposit")
                print("2. Withdraw")
                print("3. Transaction History")
                print("4. Log out")
                print("----------------------------------------\n")

                choice = input("Enter your choice: ")
                print("\n")

                if choice == '1':
                    amount = float(input("Enter deposit amount: "))
                    bank_system.deposit(account_number, amount)

                elif choice == '2':
                    amount = float(input("Enter withdrawal amount: "))
                    bank_system.withdraw(account_number, amount)

                elif choice == '3':
                    bank_system.show_transaction_history(account_number)

                elif choice == '4':
                    bank_system.log_out()
                    break

                else:
                    print("Invalid Input! Please Select 1-4 only!!!")
                    print("----------------------------------------\n")

    elif choice == '3':
        print("Thank you for using our Bank System. \nExited the Program.")
        break

    else:
        print("Invalid Input! Please Select 1-3 only!!!")
        print("\n----------------------------------------\n")
