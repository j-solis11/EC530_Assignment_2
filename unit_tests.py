import pytest
import json
from app import app, houses, rooms, devices  # Assuming your Flask app is in app.py

@pytest.fixture
def client():
    # Test client for the Flask application
    with app.test_client() as client:
        yield client


# Test for creating a device
def test_create_device(client):
    device_data = {
        'device_id': 'dev-001',
        'type': 'temperature',
        'room': None,
        'metadata': {'location': 'living room'}
    }
    
    # Test successful device creation
    response = client.post('/devices', json=device_data)
    assert response.status_code == 201
    assert 'device_id' in response.json
    assert response.json['device_id'] == 'dev-001'
    
    # Test missing fields
    device_data_missing = {
        'device_id': 'dev-002',
        'type': 'humidity'
    }
    response = client.post('/devices', json=device_data_missing)
    assert response.status_code == 400
    assert response.json['error'] == 'Missing required fields'
    
    # Test duplicate device ID
    response = client.post('/devices', json=device_data)
    assert response.status_code == 400
    assert response.json['error'] == 'Device_id already utilized'

# Test for getting device data
def test_get_device_data(client):
    device_data = {
        'device_id': 'dev-001',
        'type': 'temperature',
        'metadata': {'location': 'living room'}
    }
    client.post('/devices', json=device_data)
    
    # Test valid device retrieval
    response = client.get('/devices/dev-001')
    assert response.status_code == 200
    assert response.json['type'] == 'temperature'
    
    # Test non-existing device
    response = client.get('/devices/dev-999')
    assert response.status_code == 404
    assert response.json['error'] == 'Device not found'

# Test for editing a device
def test_edit_device(client):
    # Making house first
    house_addr = '124 Main St'
    house_data = {
        'address': '124 Main St',
        'metadata': {}
    }
    client.post('/houses', json=house_data)

    room_data = {
        'number': "101",
        'house_addr': house_addr,
        'metadata': {'size': 'large'}
    }
    
    # Test successful room creation
    client.post('/rooms', json=room_data)

    device_data = {
        'device_id': 'dev-001',
        'type': 'temperature',
        'room': None,
        'metadata': {'location': 'living room'}
    }
    
    # Test successful device creation
    client.post('/devices', json=device_data)

    # Testing edits
    edit = {
        'room_number': "101"
    }
    response = client.post('/edit/dev-001', json=edit)
    assert response.status_code == 201
    assert response.json['room'] == "101"
    
    # Test missing fields
    device_data_missing = {

    }
    response = client.post('/edit/dev-001', json=device_data_missing)
    assert response.status_code == 400
    assert response.json['error'] == 'Missing required fields'
    
    # Test incorrect device_id
    wrong_edit = {
        'room_number': "102"
    }
    response = client.post('/edit/dev-001', json=wrong_edit)
    assert response.status_code == 404
    assert response.json['error'] == 'Room number cannot be found'


# Test for creating a house
def test_create_house(client):
    house_data = {
        'address': '123 Main St',
        'metadata': {'owner': 'John Doe'}
    }
    
    # Test successful house creation
    response = client.post('/houses', json=house_data)

    # Checking for all fields
    assert response.status_code == 201
    assert 'address' in response.json
    assert response.json['address'] == '123 Main St'

    # Test missing fields
    house_data_missing = {
        'address': '456 Main St'
    }
    response = client.post('/houses', json=house_data_missing)
    assert response.status_code == 400
    assert response.get_json()['error'] == 'Missing required fields'
    
    # Test duplicate address
    response = client.post('/houses', json=house_data)
    assert response.status_code == 400
    assert response.get_json()['error'] == 'Address already utilized'

# Test for getting a house by address
def test_get_house(client):
    house_data = {
        'address': '123 Main St',
        'metadata': {'owner': 'John Doe'}
    }
    responses = client.post('/houses', json=house_data)
    
    # Test valid address retrieval
    response = client.get('/houses/123 Main St')
    assert response.status_code == 200
    assert response.json['address'] == '123 Main St'
    
    # Test non-existing address
    response = client.get('/houses/999 Fake St')
    assert response.status_code == 404
    assert response.json['error'] == 'House address not found'

# Test for creating a room
def test_create_room(client):
    # Making house first
    house_addr = '123 Main St'
    house_data = {
        'address': '123 Main St',
        'metadata': {}
    }
    client.post('/houses', json=house_data)

    room_data = {
        'number': 101,
        'house_addr': house_addr,
        'metadata': {'size': 'large'}
    }
    
    # Test successful room creation
    response = client.post('/rooms', json=room_data)
    assert response.status_code == 201
    assert 'id' in response.json
    assert response.json['number'] == 101

    # Test non-existent house address
    house_addr_incorrect = {
        'number': 101,
        'house_addr': "house_addr",
        'metadata': {'size': 'large'}
    }
    
    response = client.post('/rooms', json=house_addr_incorrect)
    assert response.status_code == 404
    assert response.json['error'] == 'House address cannot be found'
    
    # Test missing fields
    room_data_missing = {'number': 102}
    response = client.post('/rooms', json=room_data_missing)
    assert response.status_code == 400
    assert response.json['error'] == 'Missing required fields'
    
    # Test duplicate room number
    response = client.post('/rooms', json=room_data)
    assert response.status_code == 400
    assert response.json['error'] == 'Number already utilized'

# Test for getting room data
def test_get_room_data(client):
    # Making house first
    house_addr = '123 Main St'
    house_data = {
        'address': house_addr,
        'metadata': {}
    }
    client.post('/houses', json=house_data)

    room_data = {
        'number': "101",
        'house_addr': house_addr,
        'metadata': {'size': 'large'}
    }
    client.post('/rooms', json=room_data)
    
    # Test valid room retrieval
    response = client.get('/rooms/101/data')
    assert response.status_code == 200
    assert response.json['number'] == "101"
    
    # Test non-existing room
    response = client.get('/rooms/999/data')
    assert response.status_code == 404
    assert response.json['error'] == 'House not found'




