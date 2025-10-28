from http import HTTPStatus

from app.security import create_token


def test_get_token(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.username, 'password': user.clean_password},
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert 'token_type' in token


def test_unauthorized_user(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.username, 'password': 'wrong_password'},
    )

    token = response.json()

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert token == {'detail': 'Usuário ou Senha inválidos'}


def test_invalid_token(client):
    response = client.delete('/users/1', headers={'Authorization': 'Bearer token quebrado'})

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_invalid_token_by_subject(client):
    data = {'no-subject': ''}
    token = create_token(data)

    response = client.delete(
        '/users/1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_invalid_token_by_inexistent_usert(client):
    data = {'sub': 'unregistred'}
    token = create_token(data)

    response = client.delete(
        '/users/1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}
