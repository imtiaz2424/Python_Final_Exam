
from abc import ABC

# This is user class part

class User(ABC):
    def __init__(self, name, email, phone, address):
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address

    
# This is bank class part

class Bank:
    def __init__(self, name):
        self.name = name
        self.employees = []
        self.accounts = {}
        self.bank_balance = 0
        self.loan_feature = True        

    def account_email(self, email):
        return self.accounts.get(email, None)

    def transfer(self, from_email, to_email, amount):
        from_acct = self.account_email(from_email)
        to_acct = self.account_email(to_email)
        if from_acct and to_acct:
            if from_acct.balance >= amount:
                from_acct.balance -= amount
                to_acct.balance += amount
                from_acct.transactions.append(("Transfer: ", amount, to_email))
            else:
                print("Insufficient balance")
        else:
            print("Account does not exist")

    def check_bankruptcy(self):
        total_balance = sum(account.balance for account in self.accounts.values())
        if total_balance > self.bank_balance:
            print("The bank is bankrupt.")
        else:
            print("The bank is not bankrupt.")                   

    def add_employee(self, employee):        
        self.employees.append(employee)

    def view_employee(self):
        print("Employee List!")
        for emp in self.employees:
            print(emp.name, emp.email, emp.phone, emp.address)

# This is account holder part 

class Account_holder(User):
    def __init__(self, name, email, phone, address, account_type):
        super().__init__(name, email, phone, address)
        self.account_type = account_type        
        self.balance = 0
        self.total_loan = 0        
        self.loan_count = 0
        self.transactions = []                                                                      
    
    def deposit(self, amount, bank):
        self.balance += amount
        bank.bank_balance += amount        
        self.transactions.append(("Deposit: ", amount))

    def withdraw(self, amount, bank):
        if amount > self.balance:
            print("Withdrawal amount exceeded")
        else:
            self.balance -= amount
            bank.bank_balance -= amount            
            self.transactions.append(("Withdraw: ", amount))
    
    def check_balance(self):
        return self.balance

    def check_transactions(self):
        return self.transactions

    def take_loan(self, amount, bank):
        if self.loan_count < 2 and bank.loan_feature:
            self.balance += amount
            bank.bank_balance -= amount
            self.total_loan += amount
            self.loan_count += 1
            self.transactions.append(("Loan: ", amount))
        else:
            print("Loan limit exceeded")        

    
# This is employees part

class Employees(User):
    def __init__(self, name, email, phone, address, age, designation, salary):
        super().__init__(name, email, phone, address)       
        self.age = age
        self.designation = designation
        self.salary = salary  


# This is admin part

class Admin(User):
    def __init__(self, name, email, phone, address):
        super().__init__(name, email, phone, address)    

    def create_account(self, bank, name, email, phone, address, account_type):
        account = Account_holder(name, email, phone, address, account_type)
        bank.accounts[email] = account       
    
    def list_accounts(self, bank):
        return list(bank.accounts.keys())      

    def check_balance(self, bank):
        total_balance = sum(account.balance for account in bank.accounts.values())
        return total_balance    

    def total_loan(self, bank):
        total_loan = sum(account.loan_count for account in bank.accounts.values())
        return total_loan

    def loan_features(self, bank):
        bank.loan_feature = not bank.loan_feature

    def add_employee(self, bank, employee):
        bank.add_employee(employee)
    
    def view_employee(self, bank):
        bank.view_employee()    

    def delete_account(self, bank, email):
        if email in bank.accounts:            
            del bank.accounts[email]



# This is the main user and admin part

# This is the main user part

amar_bank = Bank("Amar Bank")

def account_holder():
    name = input("Enter Your Name: ")
    email = input("Enter Your Email: ")
    phone = input("Enter Your Phone: ")
    address = input("Enter Your Address: ")
    account_type = input("Enter Account Type: ")                
    acct_holder = Account_holder(name, email, phone, address, account_type)
    amar_bank.accounts[email] = acct_holder
    
    while True:
        print(f"Welcome {acct_holder.name}!!")        
        print("1. Deposit")
        print("2. Withdraw")
        print("3. Balance Check")
        print("4. Transactions")
        print("5. Take Loan")
        print("6. Fund Transfer")
        print("7. Exit")    
        
        choice = int(input("Enter Your Choice : "))
        if choice == 1:
            amount = float(input("Enter deposit amount: "))
            acct_holder.deposit(amount, amar_bank)            
        elif choice == 2:
            amount = float(input("Enter withdrawl amount: "))
            acct_holder.withdraw(amount, amar_bank)
        elif choice == 3:
            print("Your balance is: ", acct_holder.check_balance())
        elif choice == 4:
            print("Your transactions are: ", acct_holder.check_transactions())
        elif choice == 5:
            amount = float(input("Enter loan amount: "))
            acct_holder.take_loan(amount, amar_bank)
        elif choice == 6:           
            recipient_email = input("Enter recipient email: ")
            amount = float(input("Enter transfer amount: "))
            amar_bank.transfer(email, recipient_email, amount)
        elif choice == 7:            
            break
        else:
            print("Invalid Input")
            
# This is the main admin part

def admin():
    name = input("Enter Your Name : ")
    email = input("Enter Your Email : ")
    phone = input("Enter Your Phone : ")
    address = input("Enter Your Address : ")
    admin = Admin(name, email, phone, address)
    
    while True:
        print(f"Welcome {admin.name}!!")
        print("1. Create Account")
        print("2. List of User Account")
        print("3. Total Available Balance")
        print("4. Total Loan")
        print("5. Loan Feature")
        print("6. Delete Account")
        print("7. Add New Employee")
        print("8. View Employee")       
        print("9. Exit")
        
        choice = int(input("Enter Your Choice : "))
        if choice == 1:            
            name = input("Enter account holder name: ")
            email = input("Enter account holder email: ")
            phone = input("Enter account holder phone: ")
            address = input("Enter account holder address: ")
            account_type = input("Enter account holder account type: ")              
            admin.create_account(amar_bank, name, email, phone, address, account_type)
        elif choice == 2:
            print("User accounts: ", admin.list_accounts(amar_bank))
        elif choice == 3:
            print("Total bank balance is: ", admin.check_balance(amar_bank))
        elif choice == 4:
            print("Total loan amount is: ", admin.total_loan(amar_bank))
        elif choice == 5:
            admin.loan_features(amar_bank)        
        elif choice == 6:            
            account_email = input("Enter account email to delete: ")
            admin.delete_account(amar_bank, account_email)
        elif choice == 7:
            name = input("Enter employee name : ")
            phone = input("Enter employee phone : ")
            email = input("Enter employee email : ")
            designation = input("Enter employee designation : ")
            age = input("Enter employee age : ")
            salary = input("Enter employee salary : ")
            address = input("Enter employee address : ")
            employee = Employees(name, email, phone, address, age, designation, salary)
            admin.add_employee(amar_bank, employee)
        elif choice == 8:
            admin.view_employee(amar_bank)
        elif choice == 9:
            break
        else:
            print("Invalid Input")

# This is welcome front part

while True:
    print("Welcome to Amar Bank!!")
    print("1. Account Holder")
    print("2. Admin")
    print("3. Exit")
    choice = int(input("Enter your choice : "))
    if choice == 1:
        account_holder()
    elif choice == 2:
        admin()
    elif choice == 3:
        break
    else:
        print("Invalid Input!!")