from myr.base.app import (
    MyrApp,
    announce_task,
    get_function_spec,
    ENV
)


class TestApp:

    def test_basic(self):
        app = MyrApp()
        assert 'myr.base.app.announce_task' in app.tasks.regular()
        assert 'announce_task' in app.conf.beat_schedule

    def test_announcing_no_tasks(self, mocker):

        class Task:
            app = MyrApp()

        mocker.patch.object(Task.app, 'send_task')

        announce_task(Task)
        Task.app.send_task.assert_called_with(
            ENV.get('MYR_ANNOUNCE_TASK'),
            args=[{}],
            queue=ENV.get('MYR_ANNOUNCE_QUEUE'))

    def test_announcing_user_tasks(self, mocker):

        class Task:
            app = MyrApp()

        mocker.patch.object(Task.app, 'send_task')

        @Task.app.task
        def test_task(a1, a2='2'):
            pass

        announce_task(Task)
        tasks_spec = {
            test_task.name: {
                'signature': get_function_spec(test_task.run)._asdict(),
                'routing': {'queue': 'celery'}
            }
        }
        Task.app.send_task.assert_called_with(
            ENV.get('MYR_ANNOUNCE_TASK'),
            args=[tasks_spec],
            queue=ENV.get('MYR_ANNOUNCE_QUEUE'))
