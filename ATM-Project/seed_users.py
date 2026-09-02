from data_base import DataBase

def main():
    database = DataBase()
    print("Enter the details for Account you want to add.")
    while True:
        choice = int(input("0.Add account \n1.quit\nchoice: "))
        if choice != 1:
            acc_num = input("Account number: ")
            name = input("User name: ")
            pin = input("4 digit pin: ")
            database.add_account(acc_num,name, pin)
            print(f"Account added for {name} in bank.")
            continue
        else:
            print("Quit.")
            break

if __name__=="__main__":
    main()