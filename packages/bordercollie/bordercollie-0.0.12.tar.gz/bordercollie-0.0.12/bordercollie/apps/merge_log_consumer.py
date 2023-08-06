#!/usr/bin/env python3
import json

import codefast as cf
import nsq
from rich import print

from bordercollie.auth import auth


class ctx(object):
    logpath = '/tmp/merged.log'
    fh = open('/tmp/merged.log', 'a')
    cter = 0
    maxsize=2000000000

import os 
def reset_file() -> bool:
    try:
        size = int(os.path.getsize(ctx.logpath))
        if ctx.cter > 10000:
            ctx.cter = 0
            if size > ctx.maxsize:
                new_fpath = ctx.logpath + '.old'
                ctx.fh.close()
                cf.shell('mv {} {}'.format(ctx.logpath, new_fpath))
                ctx.fh = open(ctx.logpath, 'a')
                return True
    except:
        pass
    return False


def persist_data(message):
    try:
        msg = json.loads(message.body)
    except json.decoder.JSONDecodeError as e:
        print(message.body)
        cf.warning({"msg": "json loads failed", "eroor": e})
        return True
    
    ctx.cter += 1
    if ctx.cter % 10000 == 0:
        reset_file()
    ctx.fh.write(msg['log'] + '\n')
    return True


def create_reader() -> nsq.Reader:
    return nsq.Reader(message_handler=persist_data,
                      nsqd_tcp_addresses=['localhost:4150'],
                      topic='log',
                      channel='persist',
                      lookupd_poll_interval=3,
                      max_in_flight=1000)


if __name__ == '__main__':
    for _ in range(1):
        create_reader()
    nsq.run()
