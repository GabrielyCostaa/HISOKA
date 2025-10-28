from http import HTTPStatus


def test_create_reading(client, token, exam):
    reading = {
        'sensor_id': 'sensor_1',
        'value': 42.0,
        'timestamp': 1625079600.0,
    }

    response = client.post(
        f'/reading/exams/{exam.id}',
        headers={'Authorization': f'Bearer {token}'},
        json=reading,
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'sensor_id': reading['sensor_id'],
        'value': reading['value'],
        'timestamp': reading['timestamp'],
    }


def test_create_reading_unauthorized(client, exam):
    reading = {
        'sensor_id': 'sensor_1',
        'value': 42.0,
        'timestamp': 1625079600.0,
    }

    response = client.post(
        f'/reading/exams/{exam.id}',
        json=reading,
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Not authenticated'}


def test_get_readings(client, token, exam, reading):
    response = client.get(
        f'/reading/exams/{exam.id}/',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    readings = response.json()
    assert len(readings) == 1
    assert readings[0] == {
        'id': 1,
        'sensor_id': reading.sensor_id,
        'value': reading.value,
        'timestamp': reading.timestamp,
    }


def test_get_readings_unauthorized(client, exam):
    response = client.get(f'/reading/exams/{exam.id}/')
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Not authenticated'}


def test_create_bulk_readings(client, token, exam):
    list_readings = [
        {
            'sensor_id': 'sensor_1',
            'readings': [10.0, 20.0, 30.0],
            'timestamps': [1625079600.0, 1625079660.0, 1625079720.0],
        },
        {
            'sensor_id': 'sensor_2',
            'readings': [15.0, 25.0, 35.0],
            'timestamps': [1625079600.0, 1625079660.0, 1625079720.0],
        },
    ]
    response = client.post(
        f'/reading/exams/{exam.id}/bulk',
        headers={'Authorization': f'Bearer {token}'},
        json=list_readings,
    )
    assert response.status_code == HTTPStatus.CREATED
    response_data = response.json()
    assert len(response_data) == len(list_readings)
    for i, sensor_data in enumerate(list_readings):
        assert response_data[i]['sensor_id'] == sensor_data['sensor_id']
        assert response_data[i]['readings'] == sensor_data['readings']
        assert response_data[i]['timestamps'] == sensor_data['timestamps']


def test_get_bulk_readings(client, token, exam, bulk_readings):
    response = client.get(
        f'/reading/exams/{exam.id}/bulk',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    response_data = response.json()
    assert len(response_data) == len(bulk_readings)
    for i, sensor_data in enumerate(bulk_readings):
        assert response_data[i]['sensor_id'] == sensor_data.sensor_id
        assert response_data[i]['readings'] == [
            reading.value for reading in bulk_readings if reading.sensor_id == sensor_data.sensor_id
        ]
        assert response_data[i]['timestamps'] == [
            reading.timestamp for reading in bulk_readings if reading.sensor_id == sensor_data.sensor_id
        ]


def test_create_to_unexistent_exam(client, token):
    reading = {
        'sensor_id': 'sensor_1',
        'value': 42.0,
        'timestamp': 1625079600.0,
    }

    response = client.post(
        '/reading/exams/9999',
        headers={'Authorization': f'Bearer {token}'},
        json=reading,
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Exam not found'}


def test_get_readings_from_unexistent_exam(client, token):
    response = client.get(
        '/reading/exams/9999/',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Exam not found'}


def test_create_bulk_to_unexistent_exam(client, token):
    list_readings = [
        {
            'sensor_id': 'sensor_1',
            'readings': [10.0, 20.0, 30.0],
            'timestamps': [1625079600.0, 1625079660.0, 1625079720.0],
        },
    ]
    response = client.post(
        '/reading/exams/9999/bulk',
        headers={'Authorization': f'Bearer {token}'},
        json=list_readings,
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Exam not found'}


def test_get_bulk_from_unexistent_exam(client, token):
    response = client.get(
        '/reading/exams/9999/bulk',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Exam not found'}


def test_create_bulk_with_mismatched_lengths(client, token, exam):
    list_readings = [
        {
            'sensor_id': 'sensor_1',
            'readings': [10.0, 20.0],
            'timestamps': [1625079600.0],
        },
    ]
    response = client.post(
        f'/reading/exams/{exam.id}/bulk',
        headers={'Authorization': f'Bearer {token}'},
        json=list_readings,
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'timestamps and readings length mismatch for sensor sensor_1'}


def test_get_bulk_readings_unauthorized(client, exam):
    response = client.get(f'/reading/exams/{exam.id}/bulk')
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Not authenticated'}
