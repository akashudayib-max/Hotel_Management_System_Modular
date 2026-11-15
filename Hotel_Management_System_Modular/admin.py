from room import Room

class AdminModule:
    def __init__(self, hotel, username="admin", password="admin123"):
        self.hotel = hotel
        self.username = username
        self.password = password

    def login(self):
        username = input("Enter admin username: ").strip()
        password = input("Enter admin password: ")
        if username == self.username and password == self.password:
            print("Admin login successful!")
            return True
        print("Invalid admin username or password.")
        return False

    def add_room(self):
        print("\\n--- ADD ROOM ---")
        room_id = input("Enter Room ID: ").strip()
        if any(r["room_id"] == room_id for r in self.hotel.rooms):
            print("Room ID already exists.")
            return

        room_type = input("Enter Room Type (Single/Double/Deluxe): ").strip().title()
        if room_type not in ["Single", "Double", "Deluxe"]:
            print("Invalid room type.")
            return

        try:
            price = float(input("Enter Price per Day: "))
            if price <= 0:
                print("Price must be greater than zero.")
                return
        except ValueError:
            print("Enter a valid price.")
            return

        self.hotel.rooms.append(Room(room_id, room_type, price).to_dict())
        self.hotel.save_all()
        print("Room added successfully!")

    def remove_room(self):
        room_id = input("Enter Room ID to remove: ").strip()
        room = next((r for r in self.hotel.rooms if r["room_id"] == room_id), None)
        if room is None:
            print("Room does not exist.")
            return
        if not room["available"]:
            print("This room is booked. Cancel its booking first.")
            return
        self.hotel.rooms.remove(room)
        self.hotel.save_all()
        print("Room removed successfully!")

    def dashboard(self):
        while True:
            print("\\n========== ADMIN DASHBOARD ==========")
            print("1. Add Rooms")
            print("2. Remove Rooms")
            print("3. View All Rooms")
            print("4. Logout")
            choice = input("Enter your choice: ").strip()

            if choice == "1":
                self.add_room()
            elif choice == "2":
                self.remove_room()
            elif choice == "3":
                self.hotel.view_rooms()
            elif choice == "4":
                print("Admin logged out.")
                break
            else:
                print("Invalid choice.")

    def menu(self):
        while True:
            print("\\n========== ADMIN MENU ==========")
            print("1. Login")
            print("2. Back")
            choice = input("Enter your choice: ").strip()

            if choice == "1":
                if self.login():
                    self.dashboard()
            elif choice == "2":
                break
            else:
                print("Invalid choice.")
