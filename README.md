Data Structures:
House:
{
    id: Private member,
    address: Address of house,
    rooms: List of rooms,
    metadata: metadata
}

Room:
{
    id: Private member,
    number: Room number,
    house_addr: Address of house,
    devices: List of device ids in room,
    metadata: metadata
}

Device:
{
    'id': Private member,
    'device_id': ID of device
    'type': Type of device,
    'reading': Device Reading,
    'room': Device room,
    'metadata': metadata
}