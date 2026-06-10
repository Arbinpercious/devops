"""
WSGI entry point for Render deployment
"""
import os
from flask import Flask, jsonify, request
from app import BusBookingSystem

app = Flask(__name__)
bus_system = BusBookingSystem()

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'message': 'Bus Booking System API',
        'endpoints': {
            'buses': '/api/buses',
            'book': '/api/book',
            'status': '/health'
        }
    })

@app.route('/api/buses', methods=['GET'])
def get_buses():
    """Get all available buses"""
    buses_list = []
    for bus_id, details in bus_system.buses.items():
        booked_count = sum(1 for b in bus_system.bookings.values() if b['bus_id'] == bus_id)
        available = details['total_seats'] - booked_count
        buses_list.append({
            'id': bus_id,
            'name': details['name'],
            'available': available,
            'total_seats': details['total_seats'],
            'price': details['price']
        })
    return jsonify({'buses': buses_list})

@app.route('/api/book', methods=['POST'])
def book_seat():
    """Book a seat"""
    data = request.json
    bus_id = data.get('bus_id')
    seat = data.get('seat')
    passenger = data.get('passenger_name')
    
    result = bus_system.book_seat(bus_id, seat, passenger)
    return jsonify(result)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
