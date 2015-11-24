#!/usr/bin/python
#-*- coding: utf-8 -*-

from sqlalchemy import *
import sys, json,random


resp = {"success":False, "message":None}

# try:
#     create_db = create_engine('mysql+pymysql://root:test@localhost/', echo=True)
#     create_db.execute("CREATE DATABASE beyond_db")
#     resp['success']=True
#     resp['message']="DB created"
# except Exception as e:
#     resp['message']="Failed to create! %s" % e
#     print resp

try:
    db = create_engine('mysql+pymysql://root:test@localhost/beyond_db', echo=True)
    connection = db.connect()
    resp['success']=True
    resp['message']="Connected! %s" % (db.raw_connection)
    print resp
except Exception as e:
    resp['message']="Failed to connect! %s" % e
    print resp

#create tables and admin account
try:
    metadata = MetaData(bind=db)
    
    admin_table = Table('admin', metadata,Column('id',Integer, primary_key=True, nullable=False),
                          Column('username', String(20), nullable=False), 
                          Column('password', String(10),nullable=False))

    hashtag_table = Table('hashtag', metadata,Column('id',Integer, primary_key=True, nullable=False),
                          Column('hashtag', String(30), nullable=False))

    admin_hashtags_table = Table('admin_hashtags', metadata,Column('id',Integer, primary_key=True, nullable=False),
                                 Column('admin_id', Integer, nullable=False), 
                                 Column('hashstag_id', Integer,nullable=False))

    token_table = Table('token', metadata,Column('id',Integer, primary_key=True, nullable=False),
                                 Column('admin_id', Integer, nullable=False))
    
    # create tables in database
    metadata.create_all()

    admin = 0

    while admin < 2:
        username_raw = "admin"
        password_raw = "pass"
        insert = admin_table.insert()
        if admin == 0:
            username = "%s_%d" %(username_raw, 1)
            password = "%s_%d" %(password_raw, 1)
        else:
            username = "%s_%d" %(username_raw, 2)
            password = "%s_%d" %(password_raw, 2)
        new_admin = insert.values(username=username, password=password)            
        #establish database connection
        insert_statement = db.connect()
        #execute insert statement
        insert_statement.execute(new_admin)
        admin += 1
    
    resp.update({'num_admin_created':admin})
    resp['message']="admin account created"
    resp['success']=True
    print resp
except Exception as e:
    resp['success']=False
    resp['message']="failed!Reason:%s" % e
    print resp


#generate hashstags
hash_stags =["follow", "FOLLOW", "YOLO", "yolo", "win", "WIN", "pray", "PRAY"]
