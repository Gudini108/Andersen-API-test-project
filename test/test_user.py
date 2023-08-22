import unittest
import asyncio
from unittest.mock import patch
from fastapi import HTTPException

from app.routers.auth import signup
from app.db import TodoUser

test_user_1 = TodoUser(
    username='Foo',
    password='BarBar',
    first_name='Buz'
)

test_user_2_same_username = TodoUser(
    username='Foo',
    password='BuzBuz',
    first_name='Bar'
)


async def resolve(value):
    return value


class BasicTests(unittest.TestCase):
    @patch('app.routers.auth.UserRepo')
    def test_user_signup_success(self, mock_repo):
        async def async_test():

            mock_repo.safe_get_user_by_username.return_value = resolve(None)

            mock_repo.save_user.return_value = resolve(test_user_1)

            signup_result = await signup(test_user_1)

            self.assertEqual(signup_result, {
                "message": "Registration complete!"
            }, 'Successful message sent')

        asyncio.run(async_test())

    @patch('app.routers.auth.UserRepo')
    def test_user_signup_failure(self, mock_repo):
        async def async_test():

            mock_repo.safe_get_user_by_username.return_value = \
                resolve(test_user_2_same_username)

            exception = None
            try:
                await signup(test_user_1)
            except HTTPException as e:
                exception = e

            self.assertIsNotNone(exception, 'Exception thrown')

            self.assertEqual(
                409,
                exception.status_code,
                'Status code is 409 Conflict'
            )

            self.assertEqual(
                "User with this username already exists",
                exception.detail,
                'Details provided'
            )

        asyncio.run(async_test())


if __name__ == "__main__":
    unittest.main()
