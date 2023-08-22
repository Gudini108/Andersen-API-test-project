import unittest
import asyncio
from unittest.mock import patch
from fastapi import HTTPException
from pydantic import ValidationError

from app.schemas.schemas import TaskInput
from app.routers.tasks import (
    create_task,
    get_all_tasks,
    get_task,
    update_task,
    delete_task
)
from tests.common import (
    value_to_await,
    test_user_3_different_username,
    test_task_1,
    test_task_2_with_same_user,
    test_tasks_all
)


class TaskTests(unittest.TestCase):
    @patch('app.routers.tasks.TaskRepo')
    def test_task_creation_success(self, mock_repo):
        async def async_test():

            mock_repo.create_task.return_value = value_to_await(test_task_1)

            create_result = await create_task(test_task_1)

            self.assertEqual(create_result, {
                "message": f"Task '{test_task_1.title}' created!"
                }, 'Message should match expected')

        asyncio.run(async_test())

    @patch('app.routers.tasks.TaskRepo')
    def test_task_creation_failure_wrong_status(self, mock_repo):
        async def async_test():
            mock_repo.create_task.return_value = value_to_await(test_task_1)

            exception = None
            try:
                await create_task(TaskInput(
                    title='Task with wrong status',
                    status="invalid-value"
                ))
            except Exception as e:
                exception = e

            self.assertTrue(
                isinstance(exception, ValidationError),
                'Should throw validation error'
            )

        asyncio.run(async_test())

    @patch('app.routers.tasks.TaskRepo')
    def test_task_request(self, mock_repo):
        async def async_test():

            mock_repo.get_paginated_tasks.return_value = value_to_await(
                test_tasks_all
            )

            request_result = await get_all_tasks(page=1, page_size=5)

            self.assertEqual(
                request_result,
                test_tasks_all,
                'Message should match expected'
            )

        asyncio.run(async_test())

    @patch('app.routers.tasks.TaskRepo')
    def test_request_by_id_success(self, mock_repo):
        async def async_test():
            mock_repo.safe_get_task_by_id.return_value = \
                value_to_await(test_task_1)

            self.assertEqual(
                test_task_1,
                await get_task(1),
                'Should return found task'
            )

        asyncio.run(async_test())

    @patch('app.routers.tasks.TaskRepo')
    def test_request_by_id_failure(self, mock_repo):
        async def async_test():

            mock_repo.safe_get_task_by_id.return_value = \
                value_to_await(None)

            exception = None
            try:
                await get_task(1)
            except HTTPException as e:
                exception = e

            self.assertIsNotNone(
                exception,
                'Function should throw if task is not found'
            )

            self.assertEqual(
                404,
                exception.status_code,
                'Status code should be 404 Not Found'
            )

            self.assertEqual(
                "Task not found",
                exception.detail,
                'Details should match expected'
            )

        asyncio.run(async_test())

    @patch('app.routers.tasks.TaskRepo')
    def test_update_by_id_success(self, mock_repo):
        async def async_test():
            mock_repo.safe_get_task_by_id.return_value = \
                value_to_await(test_task_1)

            mock_repo.update_task.return_value = value_to_await(None)

            self.assertEqual(
                {
                    'message': f"Task '{test_task_1.title}' "
                    "updated successfully"
                },
                await update_task(
                    test_task_1.id,
                    test_task_2_with_same_user,
                    current_user=test_task_1.user
                ),
                'Should return found task'
            )

        asyncio.run(async_test())

    @patch('app.routers.tasks.TaskRepo')
    def test_update_by_id_failure_wrong_user(self, mock_repo):
        async def async_test():
            mock_repo.safe_get_task_by_id.return_value = \
                value_to_await(test_task_1)

            exception = None
            try:
                await update_task(
                    test_task_1.id,
                    test_task_2_with_same_user,
                    current_user=test_user_3_different_username
                ),
            except HTTPException as e:
                exception = e

            self.assertIsNotNone(
                exception,
                'Function should throw if it is not a task of current user'
            )

            self.assertEqual(
                403,
                exception.status_code,
                'Status code should be 403 Forbidden'
            )

            self.assertEqual(
                "Can't update other user's tasks",
                exception.detail,
                'Details should match expected'
            )

        asyncio.run(async_test())

    @patch('app.routers.tasks.TaskRepo')
    def test_update_by_id_failure_task_not_found(self, mock_repo):
        async def async_test():

            mock_repo.safe_get_task_by_id.return_value = \
                value_to_await(None)

            exception = None
            try:
                await update_task(
                    test_task_1.id,
                    test_task_2_with_same_user,
                    current_user=test_task_1.user
                )
            except HTTPException as e:
                exception = e

            self.assertIsNotNone(
                exception,
                'Function should throw if task is not found'
            )

            self.assertEqual(
                404,
                exception.status_code,
                'Status code should be 404 Not Found'
            )

            self.assertEqual(
                "Task not found",
                exception.detail,
                'Details should match expected'
            )

        asyncio.run(async_test())

    @patch('app.routers.tasks.TaskRepo')
    def test_delete_by_id_success(self, mock_repo):
        async def async_test():
            mock_repo.safe_get_task_by_id.return_value = \
                value_to_await(test_task_1)

            mock_repo.delete_task.return_value = value_to_await(None)

            self.assertEqual(
                {
                    'message': f"Task '{test_task_1.title}' "
                    "deleted successfully"
                },
                await delete_task(
                    test_task_1.id,
                    current_user=test_task_1.user
                ),
                'Should return found task'
            )

        asyncio.run(async_test())

    @patch('app.routers.tasks.TaskRepo')
    def test_delete_by_id_failure_wrong_user(self, mock_repo):
        async def async_test():
            mock_repo.safe_get_task_by_id.return_value = \
                value_to_await(test_task_1)

            exception = None
            try:
                await delete_task(
                    test_task_1.id,
                    current_user=test_user_3_different_username
                ),
            except HTTPException as e:
                exception = e

            self.assertIsNotNone(
                exception,
                'Function should throw if it is not a task of current user'
            )

            self.assertEqual(
                403,
                exception.status_code,
                'Status code should be 403 Forbidden'
            )

            self.assertEqual(
                "Can't delete other user's tasks",
                exception.detail,
                'Details should match expected'
            )

        asyncio.run(async_test())

    @patch('app.routers.tasks.TaskRepo')
    def test_delete_by_id_failure_task_not_found(self, mock_repo):
        async def async_test():

            mock_repo.safe_get_task_by_id.return_value = \
                value_to_await(None)

            exception = None
            try:
                await delete_task(
                    test_task_1.id,
                    current_user=test_task_1.user
                )
            except HTTPException as e:
                exception = e

            self.assertIsNotNone(
                exception,
                'Function should throw if task is not found'
            )

            self.assertEqual(
                404,
                exception.status_code,
                'Status code should be 404 Not Found'
            )

            self.assertEqual(
                "Task not found",
                exception.detail,
                'Details should match expected'
            )

        asyncio.run(async_test())


if __name__ == "__main__":
    unittest.main()
