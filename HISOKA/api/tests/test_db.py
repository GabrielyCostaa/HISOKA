from sqlalchemy import select

from app.models import User


def test_create_user(session):
    new_user = User(
        username='henrycke',
        email='henryckebs@gmail.com',
        password='senha_forte',
    )

    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.email == new_user.email))

    assert user.username == new_user.username
