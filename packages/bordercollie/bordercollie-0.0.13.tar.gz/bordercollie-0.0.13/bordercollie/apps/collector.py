#!/usr/bin/env python3
import time
from typing import List, Tuple

import codefast as cf
import pandas as pd
import redis
from codefast.io._json import Gzip
from simauth import OnlineAuth


class UniqRedis(object):
    _instance = None

    def init(self):
        if not self._instance:
            oa = OnlineAuth('https://cf.ddot.cc/api')
            try:
                cf.info('waiting for auth ...')
                accs = oa.auth('cn_redis')
                host, port, password = accs['host'], accs['port'], accs[
                    'password']
                self._instance = redis.Redis(host=host,
                                             port=port,
                                             password=password)
                cf.info('auth success.')
            except Exception as e:
                cf.error({'hint': 'auth failed', 'error': e})
                exit(1)
        return self._instance


def last_minute() -> str:
    now = pd.Timestamp.now()
    last_minute = now - pd.Timedelta(minutes=1)
    return last_minute.strftime('%Y-%m-%d %H:%M')


def collect_newest(log_path: str) -> Tuple[str, str]:
    last_minute_str = last_minute()
    logs = []
    with open(log_path, 'r') as f:
        for line in f:
            if line.startswith(f'[{last_minute_str}'):
                logs.append(line)
    logs = Gzip.compress({'logs': logs})
    return f'merged_log_{last_minute_str}', logs


def publish_to_redis(bredis, key: str, logs: str) -> bool:
    return bredis.setex(key, 60, logs)


def fetch_from_redis(bredis, key: str) -> bytes:
    return bredis.get(key)


def fetch_newest(bredis) -> List[str]:
    key = f'merged_log_{last_minute()}'
    bytes_ = fetch_from_redis(bredis, key)
    return Gzip.decompress(bytes_)['logs']


def main():
    LOG_PATH = '/tmp/merged.log'
    bredis = UniqRedis().init()
    while True:
        key, logs = collect_newest(LOG_PATH)
        resp = publish_to_redis(bredis, key, logs)
        cf.info(resp)
        logs = fetch_newest(bredis)
        cf.info(logs[-10:])
        time.sleep(60)


if __name__ == '__main__':
    main()
