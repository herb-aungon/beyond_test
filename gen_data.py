#!/usr/bin/python
#-*- coding: utf-8 -*-

from sqlalchemy import *
import sys, json,random, datetime
from sqlalchemy.sql import select

resp = {"success":False, "message":None}

try:
    create_db = create_engine('mysql+pymysql://root:test@localhost/', echo=True)
    create_db.execute("CREATE DATABASE beyond_db")
    resp['success']=True
    resp['message']="DB created"
except Exception as e:
    resp['message']="Failed to create! %s" % e
    print resp

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
                          Column('hashtag', String(30), nullable=False),
                          Column('date', Date(), nullable=False))

    admin_hashtags_table = Table('admin_hashtags', metadata,Column('id',Integer, primary_key=True, nullable=False),
                                 Column('admin_id', Integer, nullable=False), 
                                 Column('hashtag_id', Integer,nullable=False))

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
    sys.exit(1)

#generate hashstags
try:
    date_now = datetime.datetime.now()
    date_list = []
    d=0
    while d < 5:
        d+=1
        t = datetime.date(day=date_now.day-d, month=date_now.month, year=date_now.year)
        date_list.append(datetime.datetime.strftime(t,'%Y-%m-%d'))
    #print date_list 

    hash_stags_ins = 0
    hash_stags =["follow", "FOLLOW", "YOLO", "yolo", "win", "WIN", "pray", "PRAY", "playing", "PLAYING", "watching", "WATCHING", "tweet", "TWEET", "listening", "LISTENING", "sports", "SPORTS"]
    
    #print len(hash_stags)
    typo = ['s', 'i', 'a', 't', 'o', 'r', 'e']
    insert_hash = hashtag_table.insert()
    
    while hash_stags_ins < len(hash_stags):
        hash_tag = hash_stags[hash_stags_ins]
        new_hash_tag = insert_hash.values(hashtag ="#%s" % hash_tag, date=random.choice(date_list))
        insert_statement = db.connect()
        insert_statement.execute(new_hash_tag)
        hash_stags_ins +=1

    typo_inserted = 0
    while typo_inserted < len(hash_stags):
        hash_tag_typo = "%s%s" % ( random.choice(hash_stags), random.choice(typo) )
        new_hash_tag_typo = insert_hash.values(hashtag ="#%s" % hash_tag_typo, date=random.choice(date_list))
        insert_statement = db.connect()
        insert_statement.execute(new_hash_tag_typo)
        typo_inserted +=1
    
    resp.update({'num_typo_hashstags_inserted':typo_inserted})
    resp.update({'num_hashstags_inserted':hash_stags_ins})
    resp['message']="hashstags inserted"
    resp['success']=True
    print resp
    #sys.exit(1)
except Exception as e:
    resp['success']=False
    resp['message']="failed!Reason:%s" % e
    print resp
    sys.exit(1)

#linking hash_stags to admin account
try:
    get_admin_id = select([admin_table]) #([admin_tbl.c.id])
    result = connection.execute(get_admin_id)
    admin_list = list(result)
    
    loc = 0
    admin_id = []
    while loc < len(admin_list):
        admin = admin_list[loc][0]
        admin_id.append(admin)
        loc +=  1

    get_hashtag_id = select([hashtag_table])
    result_ = connection.execute(get_hashtag_id)
    hashtag_list = list(result_)
    loc_ = 0
    hash_tag_id = []
    
    while loc_ < len(hashtag_list):
        hash_tag = hashtag_list[loc_][0]
        hash_tag_id.append(hash_tag)
        loc_ +=  1

    c = 0
    while c < len(hash_tag_id):
        c += 1
        insert = admin_hashtags_table.insert()
        new_ad_hash = insert.values(admin_id=random.choice(admin_id),hashtag_id=random.choice(hash_tag_id))
        #establish database connection
        insert_statement_ = db.connect()
    
        # execute insert statement
        insert_statement_.execute(new_ad_hash)
        
    # print admin_id
    # print hash_tag_id
    resp.update({'num_hashtag_link_to_admin':c})
    resp['message']="hashstags linked"
    resp['success']=True
    print resp
    
except Exception as e:
    resp['success']=False
    resp['message']="failed!Reason:%s" % e
    print resp
    
