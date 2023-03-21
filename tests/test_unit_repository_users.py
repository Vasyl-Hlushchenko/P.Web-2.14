import unittest
from datetime import date, datetime, timedelta
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.database.models import User, AuthUser
from src.schemas import UserModel
from src.repository.users import (
    get_users,
    get_user,
    create_user,
    update_user,
    remove_user,
    get_users_by_some_info,
    get_birthday_per_week,
)

users = [
    User(
    first_name = "User", second_name = "Example", email = "example@gmail.com",
    phone = "0987654321", birthaday = date.today() + timedelta(days=8), description = "Some info for testing",
    authuser_id = 1),
    User(
    first_name = "User1", second_name = "Example1", email = "example1@gmail.com",
    phone = "0987654321", birthaday = date.today() + timedelta(days=3), description = "Some info for testing",
    authuser_id = 1),
    User(first_name = "User2", second_name = "Example2", email = "example2@gmail.com",
    phone = "0987654321", birthaday = date.today() + timedelta(days=1), description = "Some info for testing",
    authuser_id = 1)
    ]


class TestUsers(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = AuthUser(id=1)
        self.body = UserModel(
            first_name = "User",
            second_name = "Example",
            email = "example@gmail.com",
            phone = "0987654321",
            birthaday = date(year=1988, month=3, day=25),
            description = "Some info for testing",
            authuser_id = 1
        )

    async def test_get_users(self):
        self.session.query().filter().offset().limit().all.return_value = users
        result = await get_users(skip=0, limit=3, db=self.session, user=self.user)
        self.assertEqual(result, users)

    async def test_get_user_found(self):
        self.session.query().filter().first.return_value = self.user
        result = await get_user(user_id=self.user.id, db=self.session, user=self.user)
        self.assertEqual(result, self.user)

    async def test_get_user_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await get_user(user_id=1, db=self.session, user=self.user)
        self.assertIsNone(result)

    async def test_create_user(self):
        result = await create_user(body=self.body, db=self.session, user=self.user)
        self.assertEqual(result.first_name, self.body.first_name)
        self.assertEqual(result.second_name, self.body.second_name)
        self.assertEqual(result.email, self.body.email)
        self.assertEqual(result.phone, self.body.phone)
        self.assertEqual(result.birthaday, self.body.birthaday)
        self.assertEqual(result.description, self.body.description)
        self.assertTrue(hasattr(result, "id"))

    async def test_update_user_found(self):
        body = UserModel(
            first_name = "User4",
            second_name = "Example",
            email = "example@gmail.com",
            phone = "0987654321",
            birthaday = date(year=1988, month=3, day=25),
            description = "Some info for testing",
            authuser_id = 1
        )
        self.session.query().filter().first.return_value = self.user
        result = await update_user(user_id=self.user.id, body=body, db=self.session, user=self.user)
        self.assertEqual(result.first_name, body.first_name)
        self.assertEqual(result.second_name, body.second_name)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.phone, body.phone)
        self.assertEqual(result.birthaday, body.birthaday)
        self.assertEqual(result.description, body.description)
        self.assertTrue(hasattr(result, "id"))

    async def test_update_user_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await update_user(user_id=self.user.id, body=self.body, db=self.session, user=self.user)
        self.assertIsNone(result)

    async def test_remove_user_found(self):
        self.session.query().filter().first.return_value = self.user
        result = await remove_user(user_id=self.user.id, db=self.session, user=self.user)
        self.assertEqual(result, self.user)

    async def test_remove_user_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await remove_user(user_id=self.user.id, db=self.session, user=self.user)
        self.assertIsNone(result)

    async def test_get_users_by_some_info(self):
        self.session.query().filter().all.return_value = users
        result = await get_users_by_some_info(some_info="example1@gmail.com", db=self.session, user=self.user)
        self.assertEqual(result, [users[1]])

    async def test_get_birthday_per_week(self):
        self.session.query().filter().all.return_value = users
        result = await get_birthday_per_week(days=5, db=self.session, user=self.user)
        self.assertEqual(result, [users[1], users[2]])


if __name__ == '__main__':
    unittest.main()
