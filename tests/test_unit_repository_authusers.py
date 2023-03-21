import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.database.models import AuthUser
from src.schemas import AuthUserModel
from src.repository.authusers import (
    get_authuser_by_email,
    create_authuser,
    update_token,
    confirmed_email,
    update_avatar,
)

class TestUsers(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = AuthUser(id=1)
        self.body = AuthUserModel(
            username = "AuthUser",
            email = "example@gmail.com",
            password = "0123456789"
        )

    async def test_get_authuser_by_email_found(self):
        self.session.query().filter().first.return_value = self.user
        result = await get_authuser_by_email(email=self.user.email, db=self.session)
        self.assertEqual(result, self.user)

    async def test_get_authuser_by_email_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await get_authuser_by_email(email=self.user.email, db=self.session)
        self.assertIsNone(result)

    async def test_create_authuser(self):
        result = await create_authuser(body=self.body, db=self.session)
        self.assertEqual(result.username, self.body.username)
        self.assertEqual(result.email, self.body.email)
        self.assertEqual(result.password, self.body.password)

    async def test_update_token(self):
        self.session.query().filter().first.return_value = self.user
        token = "token"
        await update_token(user=self.user, token=token, db=self.session)
        self.assertTrue(self.user.refresh_token)
        self.assertEqual(self.user.refresh_token, token)

    async def test_confirmed_email(self):
        self.session.query().filter().first.return_value = self.user
        await confirmed_email(email=self.user.email, db=self.session)
        self.assertTrue(self.user.confirmed)

    async def test_update_avatar(self):
        self.session.query().filter().first.return_value = self.user
        url = "http://someurl.jpeg"
        result = await update_avatar(email=self.user.email, url=url, db=self.session)
        self.assertEqual(result.avatar, url)


if __name__ == '__main__':
    unittest.main()
    