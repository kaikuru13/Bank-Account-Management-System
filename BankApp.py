# Globals and Imports 
import sqlite3
loggedIn = False
user =""
loggedIn = False
global connection
connection = sqlite3.connect('Bank_Users.db')
# Database (SQL)
def getConnection():
    connection = sqlite3.connect('Bank_Users.db')

def login(user_input,pin_input):
    cursor = connection.execute("SELECT username, pin FROM bank where username='" + user_input + "' AND PIN=" + pin_input + ";")
    results = cursor.fetchall()
    print(results)
    if len(results) > 0:
        global loggedIn
        loggedIn = True
        global user
        user = user_input
        print("You are logged In")
    else:
        print("Username/PIN Invalid")

def isAccountExist(username):
    cursor= connection.execute("SELECT username FROM bank where username='" + username + "';")
    results = cursor.fetchall()
    print(results)
    if len(results) > 0:
        return True
    else:
        return False

def createAccount(username, pin, initialDeposit):
    if not isAccountExist(username):
        connection.execute("INSERT INTO BANK (PIN,USERNAME,BALANCE) VALUES ("+pin+",'"+username+"',"+initialDeposit+");")
        connection.commit()
        if isAccountExist(username):
            print("Account created successfully")
    else:
        print("Your Account Already Exist in our system")



def getBalance(username):
    if loggedIn:
        cursor = connection.execute("SELECT BALANCE FROM BANK WHERE USERNAME = '"+username+"';")
        rs = cursor.fetchone()
        return rs
    else:
        raise Exception("USER NOT LOGGED IN")

def deposit(username, amt):
    curBalance = getBalance(username)
    newAmt = curBalance[0]+amt
    if loggedIn:
        connection.execute("UPDATE BANK SET BALANCE = "+str(newAmt)+" WHERE USERNAME='"+username+"';")
        connection.commit()
        print("Your current balance is : " + str(getBalance(username)[0]))
    else:
        raise Exception("USER NOT LOGGED IN")

def withdraw(username, amt):
    curBalance = getBalance(username)
    if curBalance[0] - amt < 0:
        print("INSUFFICIENT AMOUNT TO WITHDRAW")
    else:
        if loggedIn:
            connection.execute("UPDATE BANK SET BALANCE = "+str(curBalance[0]-amt)+" WHERE USERNAME='"+username+"';")
            connection.commit()
            print("Your current balance is : " + str(getBalance(username)[0]))
        else:
            raise Exception("USER NOT LOGGED IN")
        print("Please Log in or Create an Account")

def logout():
    loggedIn = False

print("Welcome to the Bank of Kailas! ")
print("1. Log into Your Account\n2. Create an Account\n3. Check Your Balance\n4. Deposit Money\n5. Withdraw Money")
option = 0
while option != 6:
    option = input("Enter a Choice :")

    if option == '1':
        username = input("Enter Your Username :")
        pin = input("Enter Your Pin :")
        login(username,pin)
        if loggedIn:
            print("You are logged In , Welcome Kailas Bank Customer, what can we do for you ")
        else:
            print("Your login failed, please choose back the option 1 to login back")
    elif option == '2':
        usrname = input("Enter a Username :")
        pn = input("Enter a Pin:")
        initDeposit = input("Initial Amount to deposit :")
        createAccount(usrname,pn,initDeposit)
    elif option == '3':
        print("Your Current Balance is : ")
        print(getBalance(user))
    elif option == '4':
        amt = int(input("How Much Do You Want to Deposit? :"))
        deposit(user,amt)
    elif option == '5':
        at = int(input("How Much Do You Want to Withdraw ? : "))
        withdraw(user,at)
    else:
        print("INVALID CHOICE, CHOSE 1 to 5")
