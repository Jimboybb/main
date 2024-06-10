# version1
import random

class SimpleBankingSystem:

    def __init__(self):
        self.accounts = {}
        self.usernames = {}
        self.logged_in_account = None

    def generate_random_account_number(self):
        while True:
            random_account_number = random.randint(100000, 999999)
            if random_account_number not in self.accounts:
                return random_account_number

    def create_account(self, username, pin, initial_balance):
        while True:
            try:
                initial_balance = float(initial_balance)
                break
            except ValueError:
                print("Invalid input. Please enter a valid initial balance.")
                initial_balance = input("Enter initial balance: ")

        account_number = self.generate_random_account_number()

        while account_number in self.accounts or username in self.usernames:
            print("Account number or username already exists. Please try again.")
            account_number = self.generate_random_account_number()
            username = input("Enter a unique username: ")

        self.accounts[account_number] = {'Username': username, 'PIN': pin, 'Balance': initial_balance, 'TransactionHistory': []}
        self.usernames[username] = account_number
        print(f"Account created successfully. Your account number is: {account_number}")

    def log_in(self, account_number, pin):
        if account_number in self.accounts and self.accounts[account_number]['PIN'] == pin:
            self.logged_in_account = account_number
            return True
        else:
            print("Login failed. Please check your credentials.")
            return False

    def log_out(self):
        print("Successfully logged out.")
        self.logged_in_account = None

    def check_balance(self, account_number):
        print(f"Current Balance for Account {account_number} ({self.accounts[account_number]['Username']}): ₱{self.accounts[account_number]['Balance']}")

    def input_pin(self, prompt):
        while True:
            pin = input(prompt)
            if len(pin) == 4 and pin.isdigit():
                return pin
            else:
                print("Invalid PIN. Please enter a 4-digit PIN.")

# Instantiate the banking system
bank_system = SimpleBankingSystem()

# Main loop
while True:
    print("Welcome to GengGeng Bank")
    print("\nLogin Interface")
    print("1. Create Account")
    print("2. Log In")
    print("3. Exit")

    choice = input("Enter your choice: ")

    if choice == '1':
        username = input("Enter a unique username: ")
        pin = bank_system.input_pin("Set your 4-digit PIN: ")
        initial_balance = input("Enter initial balance: ")
        bank_system.create_account(username, pin, initial_balance)

    elif choice == '2':
        while True:
            account_number = input("Enter account number: ")
            if account_number.isdigit():
                account_number = int(account_number)
                break
            else:
                print("Invalid input. Account number must be a number.")
    
        pin = bank_system.input_pin("Enter your 4-digit PIN: ")
        if bank_system.log_in(account_number, pin):
            print("Login successful.\n")
            print("----------------------------------------")
    
            while True:
                print("Main Menu\n")
                bank_system.check_balance(account_number)
                print(" ")
    
                print("1. Log out")
                print("----------------------------------------\n")
    
                choice = input("Enter your choice: ")
                print("\n")
    
                if choice == '1':
                    bank_system.log_out()
                    break

                else:
                    print("Invalid Input! Please Select 1 only!!!")

    elif choice == '3':
        print("Exited the Program.")
        break

    else:
        print("Invalid Input! Please Select 1-3 only!!!")
        print(" ")
        print("----------------------------------------\n")
