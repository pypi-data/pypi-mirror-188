#!/usr/bin/env python3
import codefast as cf
import requests
from celery import Celery
from celery.schedules import crontab
from simauth import OnlineAuth

from bordercollie.auth import auth

try:
    backend = auth.celery_backend
except:
    backend = OnlineAuth('https://cf.ddot.cc/api').auth('broker')
broker = 'redis://localhost:6379'
# broker = auth.amqp

app = Celery('mycel', broker=broker, backend=backend)
app.conf.update(result_expires=10, )


@app.task
def shell(cmd: str) -> str:
    try:
        return cf.shell(cmd)
    except Exception as e:
        return str(e)


@app.task
def test(s: str):
    url = 'https://cf.ddot.cc/api/fastbark/title/msg'
    requests.get(url)


app.conf.beat_schedule = {
    "birthday-task": {
        "task": "bordercollie.mycel.test",
        "schedule": crontab(hour="*", minute="*"),
        "args": ("test", )
    }
}
