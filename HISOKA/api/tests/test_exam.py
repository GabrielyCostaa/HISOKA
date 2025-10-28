from http import HTTPStatus


def test_create_exam(client, token):
    response = client.post(
        '/exams/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'comment': 'This is a test exam',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'comment': 'This is a test exam',
        'created_at': response.json()['created_at'],
    }


def test_create_exam_unauthorized(client):
    response = client.post(
        '/exams/',
        json={
            'comment': 'This is a test exam',
        },
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Not authenticated'}


def test_get_exam(client, token, exam):
    response = client.get(
        f'/exams/{exam.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': exam.id,
        'comment': exam.comment,
        'created_at': response.json()['created_at'],
    }


def test_get_exam_unauthorized(client, exam):
    response = client.get(f'/exams/{exam.id}')
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Not authenticated'}


def test_get_nonexistent_exam(client, token):
    response = client.get(
        '/exams/999',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Exam not found'}


def test_get_exams_list(client, token, exam):
    response = client.get(
        '/exams/',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == [
        {
            'id': exam.id,
            'comment': exam.comment,
            'created_at': response.json()[0]['created_at'],
        }
    ]


def test_get_exams_list_unauthorized(client):
    response = client.get('/exams/')
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Not authenticated'}
