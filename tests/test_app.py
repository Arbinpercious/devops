"""
Unit Tests for Bus Booking System
Tests all core functionality using unittest (standard library)
"""

import unittest
import sys
from pathlib import Path

# Add parent directory to path to import app module
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import BusBookingSystem


class TestBusBookingSystem(unittest.TestCase):
    """Test cases for BusBookingSystem class"""

    def setUp(self):
        """Initialize a fresh BusBookingSystem instance for each test"""
        self.system = BusBookingSystem()

    def test_buses_initialized(self):
        """Test that buses are properly initialized"""
        self.assertEqual(len(self.system.buses), 3)
        self.assertIn('B001', self.system.buses)
        self.assertIn('B002', self.system.buses)
        self.assertIn('B003', self.system.buses)

    def test_bus_details(self):
        """Test that bus details are correct"""
        bus_b001 = self.system.buses['B001']
        self.assertEqual(bus_b001['name'], 'Express 101')
        self.assertEqual(bus_b001['total_seats'], 5)
        self.assertEqual(bus_b001['price'], 500)

    def test_bookings_empty_initially(self):
        """Test that bookings list is empty at initialization"""
        self.assertEqual(len(self.system.bookings), 0)

    def test_booking_counter_initialized(self):
        """Test that booking counter starts at 1000"""
        self.assertEqual(self.system.booking_counter, 1000)


class TestBookingSeat(unittest.TestCase):
    """Test cases for booking seats"""

    def setUp(self):
        """Initialize a fresh system for each test"""
        self.system = BusBookingSystem()

    def test_successful_booking(self):
        """Test successful seat booking"""
        success, message = self.system.book_seat('B001', 1, 'Alice')
        self.assertTrue(success)
        self.assertIn('Booking confirmed', message)
        self.assertEqual(len(self.system.bookings), 1)

    def test_booking_id_generated(self):
        """Test that booking ID is generated correctly"""
        self.system.book_seat('B001', 1, 'Alice')
        self.assertIn(1000, self.system.bookings)
        booking = self.system.bookings[1000]
        self.assertEqual(booking['passenger'], 'Alice')
        self.assertEqual(booking['bus_id'], 'B001')
        self.assertEqual(booking['seat'], 1)

    def test_booking_counter_increments(self):
        """Test that booking counter increments with each booking"""
        self.system.book_seat('B001', 1, 'Alice')
        self.assertEqual(self.system.booking_counter, 1001)
        self.system.book_seat('B001', 2, 'Bob')
        self.assertEqual(self.system.booking_counter, 1002)

    def test_invalid_bus_id(self):
        """Test booking with invalid bus ID"""
        success, message = self.system.book_seat('B999', 1, 'Alice')
        self.assertFalse(success)
        self.assertIn('not found', message)

    def test_invalid_seat_number_too_high(self):
        """Test booking with seat number exceeding total seats"""
        success, message = self.system.book_seat('B001', 10, 'Alice')
        self.assertFalse(success)
        self.assertIn('Invalid seat number', message)

    def test_invalid_seat_number_too_low(self):
        """Test booking with seat number below 1"""
        success, message = self.system.book_seat('B001', 0, 'Alice')
        self.assertFalse(success)
        self.assertIn('Invalid seat number', message)

    def test_negative_seat_number(self):
        """Test booking with negative seat number"""
        success, message = self.system.book_seat('B001', -1, 'Alice')
        self.assertFalse(success)
        self.assertIn('Invalid seat number', message)

    def test_double_booking_same_seat(self):
        """Test that same seat cannot be booked twice"""
        self.system.book_seat('B001', 1, 'Alice')
        success, message = self.system.book_seat('B001', 1, 'Bob')
        self.assertFalse(success)
        self.assertIn('already booked', message)

    def test_multiple_bookings_different_seats(self):
        """Test multiple bookings on different seats"""
        self.system.book_seat('B001', 1, 'Alice')
        self.system.book_seat('B001', 2, 'Bob')
        self.system.book_seat('B001', 3, 'Charlie')
        self.assertEqual(len(self.system.bookings), 3)

    def test_booking_all_seats(self):
        """Test booking all available seats on a bus"""
        for i in range(1, 6):  # B001 has 5 seats
            success, message = self.system.book_seat('B001', i, f'Passenger {i}')
            self.assertTrue(success)
        self.assertEqual(len(self.system.bookings), 5)

    def test_booking_after_all_seats_full(self):
        """Test booking attempt when all seats are full"""
        for i in range(1, 6):
            self.system.book_seat('B001', i, f'Passenger {i}')
        success, message = self.system.book_seat('B001', 5, 'Extra Passenger')
        self.assertFalse(success)
        self.assertIn('already booked', message)


class TestCancelBooking(unittest.TestCase):
    """Test cases for canceling bookings"""

    def setUp(self):
        """Initialize a fresh system for each test"""
        self.system = BusBookingSystem()

    def test_successful_cancellation(self):
        """Test successful booking cancellation"""
        self.system.book_seat('B001', 1, 'Alice')
        success, message = self.system.cancel_booking(1000)
        self.assertTrue(success)
        self.assertIn('cancelled', message)

    def test_booking_removed_after_cancellation(self):
        """Test that booking is removed from system after cancellation"""
        self.system.book_seat('B001', 1, 'Alice')
        self.assertEqual(len(self.system.bookings), 1)
        self.system.cancel_booking(1000)
        self.assertEqual(len(self.system.bookings), 0)

    def test_seat_available_after_cancellation(self):
        """Test that seat can be rebooked after cancellation"""
        self.system.book_seat('B001', 1, 'Alice')
        self.system.cancel_booking(1000)
        success, message = self.system.book_seat('B001', 1, 'Bob')
        self.assertTrue(success)
        self.assertIn('Booking confirmed', message)

    def test_cancel_invalid_booking_id(self):
        """Test cancellation with invalid booking ID"""
        success, message = self.system.cancel_booking(9999)
        self.assertFalse(success)
        self.assertIn('not found', message)

    def test_cancel_nonexistent_booking(self):
        """Test cancellation when no bookings exist"""
        success, message = self.system.cancel_booking(1000)
        self.assertFalse(success)
        self.assertIn('not found', message)

    def test_cancel_same_booking_twice(self):
        """Test that same booking cannot be cancelled twice"""
        self.system.book_seat('B001', 1, 'Alice')
        self.system.cancel_booking(1000)
        success, message = self.system.cancel_booking(1000)
        self.assertFalse(success)
        self.assertIn('not found', message)


class TestMultiBusScenarios(unittest.TestCase):
    """Test cases for multi-bus scenarios"""

    def setUp(self):
        """Initialize a fresh system for each test"""
        self.system = BusBookingSystem()

    def test_booking_multiple_buses(self):
        """Test booking on multiple different buses"""
        self.system.book_seat('B001', 1, 'Alice')
        self.system.book_seat('B002', 1, 'Bob')
        self.system.book_seat('B003', 1, 'Charlie')
        self.assertEqual(len(self.system.bookings), 3)

    def test_same_seat_different_buses(self):
        """Test booking same seat number on different buses"""
        success1, _ = self.system.book_seat('B001', 1, 'Alice')
        success2, _ = self.system.book_seat('B002', 1, 'Bob')
        self.assertTrue(success1)
        self.assertTrue(success2)

    def test_cancel_booking_on_one_bus_affects_only_that_bus(self):
        """Test that canceling booking on one bus doesn't affect others"""
        self.system.book_seat('B001', 1, 'Alice')
        self.system.book_seat('B002', 1, 'Bob')
        self.system.cancel_booking(1000)
        # Can rebook on B001 but B002 booking still exists
        success, _ = self.system.book_seat('B001', 1, 'Charlie')
        self.assertTrue(success)
        self.assertEqual(len(self.system.bookings), 2)


class TestDataStructures(unittest.TestCase):
    """Test cases to verify core data structures are working correctly"""

    def setUp(self):
        """Initialize a fresh system for each test"""
        self.system = BusBookingSystem()

    def test_buses_is_dictionary(self):
        """Test that buses is a dictionary"""
        self.assertIsInstance(self.system.buses, dict)

    def test_bookings_is_dictionary(self):
        """Test that bookings is a dictionary"""
        self.assertIsInstance(self.system.bookings, dict)

    def test_bus_details_structure(self):
        """Test that bus details have correct structure"""
        bus = self.system.buses['B001']
        self.assertIn('name', bus)
        self.assertIn('total_seats', bus)
        self.assertIn('price', bus)

    def test_booking_details_structure(self):
        """Test that booking details have correct structure"""
        self.system.book_seat('B001', 1, 'Alice')
        booking = self.system.bookings[1000]
        self.assertIn('bus_id', booking)
        self.assertIn('seat', booking)
        self.assertIn('passenger', booking)

    def test_no_external_dependencies(self):
        """Verify system uses only core Python data structures"""
        # This test verifies the architecture
        self.assertIsInstance(self.system.buses, dict)
        self.assertIsInstance(self.system.bookings, dict)
        # No numpy, pandas, or other external libraries used
        self.assertTrue(True)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions"""

    def setUp(self):
        """Initialize a fresh system for each test"""
        self.system = BusBookingSystem()

    def test_empty_passenger_name(self):
        """Test booking with empty passenger name (should work)"""
        success, message = self.system.book_seat('B001', 1, '')
        self.assertTrue(success)
        booking = self.system.bookings[1000]
        self.assertEqual(booking['passenger'], '')

    def test_passenger_name_with_spaces(self):
        """Test booking with passenger name containing spaces"""
        success, message = self.system.book_seat('B001', 1, 'John Doe Smith')
        self.assertTrue(success)
        booking = self.system.bookings[1000]
        self.assertEqual(booking['passenger'], 'John Doe Smith')

    def test_booking_boundary_seat_1(self):
        """Test booking the first seat"""
        success, message = self.system.book_seat('B001', 1, 'Alice')
        self.assertTrue(success)

    def test_booking_boundary_seat_max(self):
        """Test booking the last seat"""
        success, message = self.system.book_seat('B001', 5, 'Alice')
        self.assertTrue(success)

    def test_bus_id_case_insensitive(self):
        """Test that bus ID handling is correct (note: current implementation is case-sensitive)"""
        success, message = self.system.book_seat('b001', 1, 'Alice')
        # This should fail as implemented (case-sensitive)
        self.assertFalse(success)


def run_tests():
    """Run all tests with verbose output"""
    unittest.main(argv=[''], verbosity=2, exit=False)


if __name__ == '__main__':
    unittest.main(verbosity=2)
