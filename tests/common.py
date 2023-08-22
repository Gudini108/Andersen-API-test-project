from app.db import TodoUser, TodoTask


async def value_to_await(value):
    return value


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


test_user_3_different_username = TodoUser(
    username='Buz',
    password='BuzBuz',
    first_name='Bar'
)

test_task_1 = TodoTask(
    title="Foo",
    user=test_user_1
)

test_task_2_with_same_user = TodoTask(
    title="Bar",
    user=test_user_1
)

test_tasks_all = [
    test_task_1,
    test_task_2_with_same_user,
]
