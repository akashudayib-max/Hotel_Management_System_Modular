from storage import load_data, save_data

CUSTOMER_FILE = "customers.json"

class Customer:
    def __init__(self, customer_id, name, email, username, password):
        self.customer_id = str(customer_id)
        self.name = name
        self.email = email
        self.username = username
        self.password = password

    def to_dict(self):
        return {
            "customer_id": self.customer_id,
            "name": self.name,
            "email": self.email,
            "username": self.username,
            "password": self.password
        }

class CustomerModule:
    def __init__(self, hotel):
        self.hotel = hotel

    def sign_up(self):
        print("\\n--- CUSTOMER SIGN UP ---")
        customer_id = input("Enter Customer ID: ").strip()
        name = input("Enter Name: ").strip()
        email = input("Enter Email: ").strip()
        username = input("Create Username: ").strip()
        password = input("Create Password: ")

        customers = load_data(CUSTOMER_FILE)

        if not all([customer_id, name, email, username, password]):
            print("All fields are required.")
            return
        if any(c["customer_id"] == customer_id for c in customers):
            print("Customer ID already exists.")
            return
        if any(c["username"] == username for c in customers):
            print("Username already exists.")
            return
        if "@" not in email or "." not in email:
            print("Please enter a valid email address.")
            return

        customer = Customer(customer_id, name, email, username, password)
        customers.append(customer.to_dict())
        save_data(CUSTOMER_FILE, customers)
        print("Account created successfully!")

    def login(self):
        print("\\n--- CUSTOMER LOGIN ---")
        username = input("Enter Username: ").strip()
        password = input("Enter Password: ")

        for customer in load_data(CUSTOMER_FILE):
            if customer["username"] == username and customer["password"] == password:
                print(f"Welcome, {customer['name']}!")
                return customer

        print("Invalid username or password.")
        return None

    def search_room(self):
        print("\\n1. Search by Room ID")
        print("2. Search by Room Type")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            value = input("Enter Room ID: ").strip()
            matches = [r for r in self.hotel.rooms if r["room_id"] == value]
        elif choice == "2":
            value = input("Enter Room Type: ").strip().lower()
            matches = [r for r in self.hotel.rooms if r["room_type"].lower() == value]
        else:
            print("Invalid choice.")
            return

        if not matches:
            print("No matching room found.")
            return

        for room in matches:
            status = "Available" if room["available"] else "Booked"
            print(f"Room: {room['room_id']} | Type: {room['room_type']} | "
                  f"Price/day: Rs. {room['price']:.2f} | Status: {status}")

    def book_room(self, customer):
        self.hotel.view_rooms(available_only=True)
        room_id = input("Enter Room ID to book: ").strip()

        room = next((r for r in self.hotel.rooms if r["room_id"] == room_id), None)
        if room is None:
            print("Room does not exist.")
            return
        if not room["available"]:
            print("This room is already booked.")
            return

        try:
            days = int(input("Enter number of days: "))
            if days <= 0:
                print("Days must be greater than zero.")
                return
        except ValueError:
            print("Enter a valid number of days.")
            return

        total = room["price"] * days
        booking = {
            "customer_id": customer["customer_id"],
            "customer_name": customer["name"],
            "room_id": room_id,
            "room_type": room["room_type"],
            "days": days,
            "total_amount": total
        }
        self.hotel.bookings.append(booking)
        room["available"] = False
        self.hotel.save_all()

        print("\\nRoom booked successfully!")
        print(f"Number of days: {days}")
        print(f"Total amount: Rs. {total:.2f}")

    def cancel_booking(self, customer):
        active = [b for b in self.hotel.bookings
                  if b["customer_id"] == customer["customer_id"]]
        if not active:
            print("You do not have any active bookings.")
            return

        print("\\n--- YOUR BOOKINGS ---")
        for booking in active:
            print(f"Room ID: {booking['room_id']} | "
                  f"Type: {booking['room_type']} | Days: {booking['days']}")

        room_id = input("Enter Room ID to cancel: ").strip()
        booking = next((b for b in active if b["room_id"] == room_id), None)
        if booking is None:
            print("Booking not found.")
            return

        self.hotel.bookings.remove(booking)
        for room in self.hotel.rooms:
            if room["room_id"] == room_id:
                room["available"] = True
                break
        self.hotel.save_all()
        print("Booking cancelled successfully.")

    def dashboard(self, customer):
        while True:
            print("\\n========== CUSTOMER DASHBOARD ==========")
            print("1. View All Rooms")
            print("2. Search a Room")
            print("3. Book a Room")
            print("4. Cancel Booking")
            print("5. Logout")
            choice = input("Enter your choice: ").strip()

            if choice == "1":
                self.hotel.view_rooms(available_only=True)
            elif choice == "2":
                self.search_room()
            elif choice == "3":
                self.book_room(customer)
            elif choice == "4":
                self.cancel_booking(customer)
            elif choice == "5":
                print("Customer logged out.")
                break
            else:
                print("Invalid choice.")
