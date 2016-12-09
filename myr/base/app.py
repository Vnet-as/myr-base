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


def announce_task(self):
    """Celery task for announcing user tasks to discovery service"""
    all_tasks = self.tasks.regular()
    user_tasks = {}
    for t in all_tasks:
        if t.startswith('celery.'):
            continue
        if t == 'myr.base.app.announce_task':
            continue
        user_tasks[t] = {
            'signature': get_function_spec(all_tasks[t].run)._asdict(),
            'routing': {'queue': list(self.amqp.queues.keys())[0]}
        }
    self.send_task(ENV.get('MYR_ANNOUNCE_TASK'),
                   args=[user_tasks],
                   queue=ENV.get('MYR_ANNOUNCE_QUEUE'))


class MyrApp(celery.Celery):
    def on_init(self):
        self._tasks.register(self.task(announce_task, bind=True))
        self.conf.beat_schedule = {
            'announce_task': {
                'task': 'myr.base.app.announce_task',
                'schedule': ENV.get('MYR_ANNOUNCE_INTERVAL')
            }
        }
