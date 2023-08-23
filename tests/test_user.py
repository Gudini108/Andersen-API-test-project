import unittest
import asyncio
from unittest.mock import patch
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.routers.auth import signup, login
from app.routers.users import get_all_users
from tests.common import test_user_1, test_user_2_same_username, value_to_await


class UserTests(unittest.TestCase):
    @patch('app.routers.auth.UserRepo')
    def test_user_signup_success(self, mock_repo):
        async def async_test():

            mock_repo.safe_get_user_by_username.return_value = \
                value_to_await(None)

            mock_repo.save_user.return_value = value_to_await(test_user_1)

            signup_result = await signup(test_user_1)

            self.assertEqual(signup_result, {
                "message": "Registration complete!"
            }, 'Message should match expected')

        asyncio.run(async_test())

    @patch('app.routers.auth.UserRepo')
    def test_user_signup_failure(self, mock_repo):
        async def async_test():

            mock_repo.safe_get_user_by_username.return_value = \
                value_to_await(test_user_2_same_username)

            exception = None
            try:
                await signup(test_user_1)
            except HTTPException as e:
                exception = e

            self.assertIsNotNone(
                exception,
                'Function should throw if username is used already'
            )

            self.assertEqual(
                409,
                exception.status_code,
                'Status code should be 409 Conflict'
            )

            self.assertEqual(
                "User with this username already exists",
                exception.detail,
                'Details should match expected'
            )

        asyncio.run(async_test())

    @patch('app.routers.auth.UserRepo')
    async def test_user_login_success(self, mock_repo):
        async def async_test():
            mock_repo.safe_get_user_by_username.return_value = value_to_await(
                test_user_1
            )

            login_result = await login(OAuth2PasswordRequestForm(
                username=test_user_1.username, password="password"))

            self.assertEqual(login_result, {
                "access_token": "token",
                "token_type": "bearer"
            }, 'Response should match expected')

        asyncio.run(async_test())

    @patch('app.routers.auth.UserRepo')
    async def test_user_login_failure(self, mock_repo):
        async def async_test():
            mock_repo.safe_get_user_by_username.return_value = value_to_await(
                None
            )

            try:
                await login(OAuth2PasswordRequestForm(
                    username="nonexistent_user", password="password"))
            except Exception as e:
                exception = e

            self.assertEqual(
                exception.status_code,
                401,
                'Status code should be 401 Unauthorized'
            )

            self.assertEqual(
                exception.detail,
                "Incorrect username or password",
                'Details should match expected'
            )

        asyncio.run(async_test())

    @patch('app.routers.users.UserRepo')
    def test_get_all_users_success(self, mock_user_repo):
        async def async_test():
            mock_user_repo.get_all_users.return_value = value_to_await([
                test_user_1,
                test_user_2_same_username,
            ])

            response = await get_all_users()

            self.assertEqual(len(response), 2)

        asyncio.run(async_test())


if __name__ == "__main__":
    unittest.main()
