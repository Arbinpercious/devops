"""
Mini CLI-based Bus Booking System with Environment Variables Support
Uses only core Python data structures (dict, list, tuple, set)
"""

import os
import sys

class BusBookingSystem:
    def __init__(self):
        # Load configuration from environment variables
        self.buses = self._load_buses_from_env()
        self.bookings = {}
        self.booking_counter = self._get_booking_counter()
        
    def _load_buses_from_env(self):
        """Load bus configuration from environment variables"""
        # Default buses (fallback if no env vars)
        default_buses = {
            'B001': {'name': 'Express 101', 'total_seats': 5, 'price': 500},
            'B002': {'name': 'Super Fast 202', 'total_seats': 5, 'price': 600},
            'B003': {'name': 'Comfort 303', 'total_seats': 5, 'price': 700},
        }
        
        buses = {}
        
        # Check for custom bus configurations in environment variables
        bus_keys = [key for key in os.environ.keys() if key.startswith('BUS_')]
        
        if bus_keys:
            # Parse environment variables for buses
            bus_ids = set()
            for key in bus_keys:
                parts = key.split('_')
                if len(parts) >= 2:
                    bus_ids.add(parts[1])
            
            for bus_id in bus_ids:
                bus_name = os.environ.get(f'BUS_{bus_id}_NAME', f'Bus {bus_id}')
                total_seats = int(os.environ.get(f'BUS_{bus_id}_SEATS', 5))
                price = float(os.environ.get(f'BUS_{bus_id}_PRICE', 500))
                buses[bus_id] = {
                    'name': bus_name,
                    'total_seats': total_seats,
                    'price': price
                }
            
            if buses:
                return buses
        
        # Fallback to default buses
        return default_buses
    
    def _get_booking_counter(self):
        """Get starting booking counter from environment variable"""
        return int(os.environ.get('BOOKING_START_ID', 1000))
    
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
        del self.bookings[booking_id]
        return True, f"✅ Booking {booking_id} cancelled! Seat {booking['seat']} is now available."

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
    
    def show_config(self):
        """Display current configuration from environment variables"""
        print("\n" + "="*60)
        print("CURRENT CONFIGURATION")
        print("="*60)
        print(f"Booking Start ID: {self.booking_counter}")
        print(f"Environment: {os.environ.get('ENVIRONMENT', 'development')}")
        print(f"App Version: {os.environ.get('APP_VERSION', '1.0.0')}")
        print("="*60 + "\n")


def main():
    """Main CLI menu"""
    system = BusBookingSystem()
    
    # Show configuration on startup if DEBUG mode is enabled
    if os.environ.get('DEBUG', 'False').lower() == 'true':
        system.show_config()
    
    while True:
        print("\n" + "🚌 BUS BOOKING SYSTEM 🚌".center(40))
        print("-" * 40)
        print("1. View Available Buses")
        print("2. View Bus Seats")
        print("3. Book a Seat")
        print("4. View My Bookings")
        print("5. Cancel Booking")
        print("6. Show Configuration")
        print("7. Exit")
        print("-" * 40)
        
        choice = input("Enter your choice (1-7): ").strip()
        
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
            system.show_config()
        
        elif choice == '7':
            print("\n👋 Thank you for using Bus Booking System! Goodbye!\n")
            break
        
        else:
            print("❌ Invalid choice! Please try again.")


if __name__ == "__main__":
    main()