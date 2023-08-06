#!/usr/bin/env python3
import json
import sqlite3

import codefast as cf
import joblib
import nsq
import numpy as np
import pandas as pd
from rich import print

from bordercollie.auth import auth


def get_db_conn():
    today = pd.Timestamp.today().strftime('%Y%m%d')
    dbfile = 'local/data/transcription_records_{}_{}.db'.format(cf.shell('hostname'), today)
    tmp_dbfile = '/tmp/transcription_records.db'.format(cf.shell('hostname'))
    try:
        cf.io.copy(tmp_dbfile, dbfile)
    except FileNotFoundError:
        pass  # no tmp db file
    db = sqlite3.connect(tmp_dbfile)
    db.execute(
        'create table if not exists trans_records (md5 text primary key, msg text)'
    )
    return db


db = get_db_conn()


def persist_data(message):
    try:
        msg = json.loads(message.body)
    except json.decoder.JSONDecodeError as e:
        cf.warning({"msg": "json loads failed", "eroor": e})
        return True

    md5 = cf.md5sum(str(msg))
    db.execute(
        'insert into trans_records (md5, msg) values (?, ?) on conflict (md5) do nothing',
        (md5, str(msg)))
    db.commit()
    cf.info('data {} was persisted'.format(str(msg)))
    return True


if __name__ == '__main__':
    r = nsq.Reader(message_handler=persist_data,
                   lookupd_http_addresses=[auth.nsqlookupd],
                   nsqd_tcp_addresses=[auth.nsqd_tcp],
                   topic='transcript_record',
                   channel='persist',
                   lookupd_poll_interval=3,
                   max_in_flight=10)
    nsq.run()
