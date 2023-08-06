import asyncio
import datetime

from optscale_arcee.sender.sender import Sender
from optscale_arcee.name_generator import NameGenerator


def single(class_):
    instances = {}

    def get_instance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return get_instance


@single
class Arcee:
    def __init__(self, token=None, application_key=None, endpoint_url=None, ssl=True):
        self.token = token
        self.application_key = application_key
        self.sender = Sender(endpoint_url, ssl)
        self._run = None
        self._tags = {}
        self._name = None

    @property
    def run(self):
        return self._run

    @run.setter
    def run(self, value):
        self._run = value

    @property
    def tags(self):
        return self._tags

    @tags.setter
    def tags(self, value):
        k, v = value
        self._tags.update({k: v})

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value


def init(token, application_key, run_name=None, endpoint_url=None, ssl=True):
    arcee = Arcee(token, application_key, endpoint_url, ssl)
    name = run_name if run_name is not None else NameGenerator.get_random_name()
    run_id = asyncio.run(arcee.sender.get_run_id(application_key, token, name))["id"]
    arcee.run = run_id
    arcee.name = name


def tag(key, value):
    arcee = Arcee()
    arcee.tags = (key, value)
    asyncio.run(arcee.sender.add_tags(arcee.run, arcee.token, arcee.tags))


def milestone(value):
    arcee = Arcee()
    asyncio.run(arcee.sender.add_milestone(arcee.run, arcee.token, value))


def stage(name):
    arcee = Arcee()
    asyncio.run(arcee.sender.create_stage(arcee.run, arcee.token, name))


def finish():
    arcee = Arcee()
    asyncio.run(
        arcee.sender.change_state(
            arcee.run,
            arcee.token,
            2,
            int(datetime.datetime.utcnow().timestamp()),
        )
    )


def error():
    arcee = Arcee()
    asyncio.run(
        arcee.sender.change_state(
            arcee.run,
            arcee.token,
            3,
            int(datetime.datetime.utcnow().timestamp()),
        )
    )


def info():
    arcee = Arcee()
    return arcee.__dict__


def send(data):
    arcee = Arcee()
    asyncio.run(
        arcee.sender.send_stats(
            arcee.token,
            {"project": arcee.application_key, "run": arcee.run, "data": data},
        )
    )
