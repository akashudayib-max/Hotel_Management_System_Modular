class Room:
    def __init__(self, room_id, room_type, price, available=True):
        self.room_id = str(room_id)
        self.room_type = room_type
        self.price = float(price)
        self.available = bool(available)

    def to_dict(self):
        return {
            "room_id": self.room_id,
            "room_type": self.room_type,
            "price": self.price,
            "available": self.available
        }
