from http import HTTPStatus

from app.schemas import UserPublic


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'alice',
        'email': 'alice@example.com',
        'id': 1,
    }


def test_create_duplicated_user(client, user):
    response = client.post(
        '/users/',
        json={
            'username': user.username,
            'email': user.email,
            'password': user.password,
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username or Email already exists'}


def test_update_user_to_with_existent_mail(client, user, token):
    client.post(
        '/users/',
        json={
            'username': 'another',
            'email': 'another@mail.com',
            'password': 'anohter_pass',
        },
    )

    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'another',
            'email': 'another@mail.com',
            'password': user.password,
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Username or Email already exists'}


def test_update_user(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'another',
            'email': 'another@mail.com',
            'password': user.password,
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'username': 'another', 'email': 'another@mail.com', 'id': 1}


def test_delete_user(client, user, token):
    response = client.delete(f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'})

    assert response.json() == {'message': 'User deleted'}


def test_read_users(client):
    response = client.get('/users')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')
    assert response.json() == {'users': [user_schema]}


def test_read_user_profile(client, user, token):
    expected = {'username': user.username, 'id': user.id, 'email': user.email}
    response = client.get('/users/profile', headers={'Authorization': f'Bearer {token}'})
    assert response.json() == expected


# def test_proposital():
#     assert 1 == 0
