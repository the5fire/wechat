#!/usr/bin/env python
#coding:utf-8

import sqlite3

con = sqlite3.connect('wechat.db')
cur = con.cursor()

command = """
BEGIN;
CREATE TABLE IF NOT EXISTS user(
    "id" integer PRIMARY KEY AUTOINCREMENT,
    "username" varchar(20) NOT NULL,
    "password" varchar(50) NOT NULL,
    "registed_time" datetime NOT NULL,
    UNIQUE ("username")
);
CREATE TABLE IF NOT EXISTS topic(
    "id" integer PRIMARY KEY AUTOINCREMENT,
    "title" varchar(20) NOT NULL,
    "created_time" datetime NOT NULL,
    "owner_id" integer NOT NULL,
    UNIQUE ("title", 'owner_id')
);
CREATE TABLE IF NOT EXISTS message(
    "id" integer PRIMARY KEY AUTOINCREMENT,
    "content" text NOT NULL,
    "topic_id" integer NOT NULL,
    "user_id" integer NOT NULL,
    "created_time" datetime NOT NULL
);
COMMIT;
"""

try:
    cur.executescript(command)
    con.commit()
except Exception as e:
    print e

cur.close()
con.close()
