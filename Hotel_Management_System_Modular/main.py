from hotel import Hotel
from admin import AdminModule
from customer import CustomerModule

def main():
    hotel = Hotel()
    admin = AdminModule(hotel)
    customer = CustomerModule(hotel)

    while True:
        print("\\n========== HOTEL MANAGEMENT SYSTEM ==========")
        print("1. Admin")
        print("2. Customer")
        print("3. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            admin.menu()
        elif choice == "2":
            while True:
                print("\\n========== CUSTOMER MENU ==========")
                print("1. Sign Up")
                print("2. Login")
                print("3. Back")
                customer_choice = input("Enter your choice: ").strip()

                if customer_choice == "1":
                    customer.sign_up()
                elif customer_choice == "2":
                    logged_in_customer = customer.login()
                    if logged_in_customer:
                        customer.dashboard(logged_in_customer)
                elif customer_choice == "3":
                    break
                else:
                    print("Invalid choice.")
        elif choice == "3":
            hotel.save_all()
            print("Thank you for using the Hotel Management System!")
            break
        else:
            print("Invalid choice. Please enter 1, 2 or 3.")

if __name__ == "__main__":
    main()
