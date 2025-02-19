from flask import Flask, request, jsonify

app = Flask(__name__)

houses = []
rooms = []
devices = []


@app.route('/edit/<device_id>', methods=['POST'])
def edit_device_data(device_id):
    data = request.json
    if 'room_number' not in data:
        return jsonify({"error": "Missing required fields"}), 400

    deviceToEdit = None
    for device in devices:
        if device['device_id'] == device_id:
            deviceToEdit = device
    if deviceToEdit is None:
        return jsonify({"error": "Device not found"}), 404
    

    # Testing if a room number is entered, whether it is correct
    if data['room_number'] is not None:
        roomFound = False
        for room in rooms:
            if data['room_number'] == room['number']:
                roomFound = True
        if roomFound is False:
            return jsonify({"error": "Room number cannot be found"}), 404

        
    nestedRoomNumber = None
    if deviceToEdit['room'] is not None: 
        for room in rooms:
            if deviceToEdit['room'] == room['number']:
                room['devices'].remove(deviceToEdit['device_id'])

    deviceToEdit['room'] = data['room_number']
    return jsonify(deviceToEdit), 201


@app.route('/devices', methods=['POST'])
def create_device():
    data = request.json
    if 'type' not in data or 'device_id' not in data or 'metadata' not in data or 'room' not in data:
        return jsonify({"error": "Missing required fields"}), 400
    


    # Error handling for duplicate address
    for device in devices:
        if device['device_id'] == data['device_id']:
            return jsonify({"error": "Device_id already utilized"}), 400
        
    private_id = str(len(devices) + 1)
    device = {
        'id': private_id,
        'device_id': data['device_id'],
        'type': data['type'],
        'reading': None,
        'room': data['room'],
        'metadata': data['metadata']
    }

    # Testing if a room number is entered, whether it is correct
    nestedRoomNumber = None
    if data['room'] is not None: 
        for room in rooms:
            if data['room'] == room['number']:
                nestedRoomNumber = room['number']
                dupeDevice = False
                for device in room['devices']:
                    if device == device['device_id']:
                        dupeDevice = True
                        return jsonify({"error": f"Room {room['number']} has duplicate device id"}), 400
                if dupeDevice is False:
                    room['devices'].append(device)
        if nestedRoomNumber is None:
            return jsonify({"error": "Room number cannot be found"}), 404
    
    devices.append(device)
    return jsonify(device), 201

@app.route('/devices/<device_id>', methods=['GET'])
def get_device_data(device_id):
    for device in devices:
        if device['device_id'] == device_id:
            return jsonify(device), 200
    return jsonify({'error': 'Device not found'}), 404

@app.route('/rooms', methods=['POST'])
def create_room():
    data = request.json
    if 'number' not in data or 'metadata' not in data or 'house_addr' not in data:
        return jsonify({"error": "Missing required fields"}), 400
    nestedHouse = None
    for house in houses:
        if house['address'] == data['house_addr']:
            nestedHouse = house 
    if nestedHouse == None:
        return jsonify({"error": "House address cannot be found"}), 404
    
    # Error handling for duplicate numbers
    for room in rooms:
        if room['number'] == data['number']:
            return jsonify({"error": "Number already utilized"}), 400
    room_id = str(len(rooms) + 1)
    room = {
        'id': room_id,
        'number': data['number'],
        'house_addr': nestedHouse['address'],
        'devices': [],
        'metadata': data['metadata']
    }
    nestedHouse['rooms'].append(room['number'])
    rooms.append(room)
    return jsonify(room), 201

@app.route('/rooms/<room_number>/data', methods=['GET'])
def get_room_data(room_number):
    print(f"{room_number}")
    for room in rooms:
        if room['number'] == str(room_number):
            print(room_number)
            device_ids = []
            device_readings = []
            for device in room['devices']:
                device_ids.append(f"{device['device_id']}")
                device_readings.append(f"{device['reading']}")
            return jsonify({'id': room['id'], 'number': room['number'], 'devices': room['devices'], 'metadata': room['metadata'], 'device_ids':device_ids, 'device_readings':device_readings}), 200
    return jsonify({'error': 'House not found'}), 404





@app.route('/houses', methods=['POST'])
def create_house():
    data = request.json
    print("A")
    if 'address' not in data or 'metadata' not in data:
        return jsonify({"error": "Missing required fields"}), 400
    print("A")
    # Error handling for duplicate address
    for house in houses:
        if house['address'] == data['address']:
            return jsonify({"error": "Address already utilized"}), 400
    print("A")
    house_id = str(len(houses) + 1)
    house = {
        'id': house_id,
        'address': data['address'],
        'rooms': [],
        'metadata': data['metadata']
    }
    print("A")
    houses.append(house)
    return jsonify(house), 201

@app.route('/houses/<house_addr>', methods=['GET'])
def get_house(house_addr):
    for house in houses:
        if house['address'] == house_addr:
            return jsonify(house), 200
    return jsonify({'error': 'House address not found'}), 404



if __name__ == '__main__':
    app.run(debug=True)