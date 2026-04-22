"""
Mini CLI-based Bus Booking System
Uses only core Python data structures (dict, list, tuple, set)
"""

class BusBookingSystem:
    def __init__(self):
        # Store buses: {bus_id: {'name': str, 'seats': int, 'price': float}}
        self.buses = {
            'B001': {'name': 'Express 101', 'total_seats': 5, 'price': 500},
            'B002': {'name': 'Super Fast 202', 'total_seats': 5, 'price': 600},
            'B003': {'name': 'Comfort 303', 'total_seats': 5, 'price': 700},
        }
        
        # Store bookings: {booking_id: {'bus_id': str, 'seat': int, 'passenger': str}}
        self.bookings = {}
        self.booking_counter = 1000

    def display_buses(self):
        """Display all available buses"""
        print("\n" + "="*60)
        print("AVAILABLE BUSES")
        print("="*60)
        for bus_id, details in self.buses.items():
            booked_count = sum(1 for b in self.bookings.values() if b['bus_id'] == bus_id)
            available = details['total_seats'] - booked_count
            print(f"ID: {bus_id} | Name: {details['name']} | Available: {available}/{details['total_seats']} | Price: ₹{details['price']}")
        print("="*60 + "\n")

    def display_bus_seats(self, bus_id):
        """Display seat status for a specific bus"""
        if bus_id not in self.buses:
            print(f"❌ Bus {bus_id} not found!")
            return
        
        bus = self.buses[bus_id]
        print(f"\n📍 Bus: {bus['name']} (ID: {bus_id})")
        print("Seat Status: ", end="")
        
        booked_seats = set(b['seat'] for b in self.bookings.values() if b['bus_id'] == bus_id)
        
        for seat in range(1, bus['total_seats'] + 1):
            if seat in booked_seats:
                print("❌", end=" ")
            else:
                print(f"✓{seat}", end=" ")
        print("\n")

    def book_seat(self, bus_id, seat, passenger_name):
        """Book a seat on a bus"""
        if bus_id not in self.buses:
            return False, f"❌ Bus {bus_id} not found!"
        
        bus = self.buses[bus_id]
        if seat < 1 or seat > bus['total_seats']:
            return False, f"❌ Invalid seat number! Available seats: 1-{bus['total_seats']}"
        
        # Check if seat already booked
        for booking in self.bookings.values():
            if booking['bus_id'] == bus_id and booking['seat'] == seat:
                return False, f"❌ Seat {seat} already booked!"
        
        booking_id = self.booking_counter
        self.booking_counter += 1
        self.bookings[booking_id] = {'bus_id': bus_id, 'seat': seat, 'passenger': passenger_name}
        return True, f"✅ Booking confirmed! Booking ID: {booking_id} | Seat: {seat} | Price: ₹{bus['price']}"

    def cancel_booking(self, booking_id):
        """Cancel a booking"""
        if booking_id not in self.bookings:
            return False, f"❌ Booking ID {booking_id} not found!"
        
        booking = self.bookings[booking_id]
        bus_id = booking['bus_id']
        seat = booking['seat']
        passenger = booking['passenger']
        
        del self.bookings[booking_id]
        return True, f"✅ Booking {booking_id} cancelled! Seat {seat} is now available."

    def view_bookings(self):
        """Display all current bookings"""
        if not self.bookings:
            print("\n📋 No bookings yet!\n")
            return
        
        print("\n" + "="*80)
        print("MY BOOKINGS")
        print("="*80)
        for booking_id, details in self.bookings.items():
            bus_info = self.buses[details['bus_id']]
            print(f"Booking ID: {booking_id} | Bus: {bus_info['name']} | Seat: {details['seat']} | Passenger: {details['passenger']} | Price: ₹{bus_info['price']}")
        print("="*80 + "\n")


def main():
    """Main CLI menu"""
    system = BusBookingSystem()
    
    while True:
        print("\n" + "🚌 BUS BOOKING SYSTEM 🚌".center(40))
        print("-" * 40)
        print("1. View Available Buses")
        print("2. View Bus Seats")
        print("3. Book a Seat")
        print("4. View My Bookings")
        print("5. Cancel Booking")
        print("6. Exit")
        print("-" * 40)
        
        choice = input("Enter your choice (1-6): ").strip()
        
        if choice == '1':
            system.display_buses()
        
        elif choice == '2':
            system.display_buses()
            bus_id = input("Enter Bus ID: ").strip().upper()
            system.display_bus_seats(bus_id)
        
        elif choice == '3':
            system.display_buses()
            bus_id = input("Enter Bus ID: ").strip().upper()
            try:
                seat = int(input("Enter Seat Number: ").strip())
                passenger = input("Enter Passenger Name: ").strip()
                success, message = system.book_seat(bus_id, seat, passenger)
                print(message)
            except ValueError:
                print("❌ Please enter a valid seat number!")
        
        elif choice == '4':
            system.view_bookings()
        
        elif choice == '5':
            try:
                booking_id = int(input("Enter Booking ID to cancel: ").strip())
                success, message = system.cancel_booking(booking_id)
                print(message)
            except ValueError:
                print("❌ Please enter a valid Booking ID!")
        
        elif choice == '6':
            print("\n👋 Thank you for using Bus Booking System! Goodbye!\n")
            break
        
        else:
            print("❌ Invalid choice! Please try again.")


if __name__ == "__main__":
    main()
