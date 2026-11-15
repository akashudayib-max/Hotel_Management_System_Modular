from storage import load_data, save_data

class Hotel:
    def __init__(self):
        self.rooms = load_data("rooms.json")
        self.bookings = load_data("bookings.json")

    def save_all(self):
        save_data("rooms.json", self.rooms)
        save_data("bookings.json", self.bookings)

    def view_rooms(self, available_only=False):
        rooms = [r for r in self.rooms if not available_only or r["available"]]
        if not rooms:
            print("No rooms found.")
            return

        print("\\n" + "-" * 65)
        print(f"{'Room ID':<12}{'Room Type':<15}{'Price/Day':<15}{'Status':<12}")
        print("-" * 65)
        for room in rooms:
            status = "Available" if room["available"] else "Booked"
            print(f"{room['room_id']:<12}{room['room_type']:<15}"
                  f"{room['price']:<15.2f}{status:<12}")
        print("-" * 65)
