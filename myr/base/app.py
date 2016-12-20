import celery
import inspect
import os


ENV = {
    'MYR_ANNOUNCE_TASK': 'myr.discovery.announce',
    'MYR_ANNOUNCE_QUEUE': 'announce',
    'MYR_ANNOUNCE_INTERVAL': 2.0
}
ENV.update(os.environ)


def get_function_spec(callable):
    """Returns function (callable) argspec"""
    return inspect.getargspec(callable)


def announce(self):
    """Celery task for announcing user tasks to discovery service"""
    all_tasks = self.app.tasks.regular()
    user_tasks = {}
    for task in all_tasks:
        if task.startswith('celery.'):
            continue
        if task == 'myr.base.app.announce':
            continue
            'routing': {'queue': list(self.app.amqp.queues.keys())[0]}
        user_tasks[task] = {
            'signature': get_function_spec(all_tasks[task].run)._asdict(),
        }
    self.app.send_task(ENV.get('MYR_ANNOUNCE_TASK'),
                   args=[user_tasks],
                   queue=ENV.get('MYR_ANNOUNCE_QUEUE'))


class MyrApp(celery.Celery):
    def on_init(self):
        self._tasks.register(self.task(announce, bind=True))
        self.conf.beat_schedule = {
            'announce': {
                'task': 'myr.base.app.announce',
                'schedule': ENV.get('MYR_ANNOUNCE_INTERVAL')
            }
        }
