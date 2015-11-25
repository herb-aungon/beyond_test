#!/usr/bin/env python
#-*- coding: utf-8 -*-
from sqlalchemy import *
import sys, json,random, datetime, enchant

#simple security check(checks if the toekn is valid)
class token():
    def __init__(self):
        self.__db = create_engine('mysql+pymysql://root:test@localhost/beyond_db', echo=True)
        self.__connection = self.__db.connect()
        self.__result = {'success':False, 'message':None, 'data':None}
    def token_validator(self, token):
        try:
            find_tok=("""SELECT * 
            FROM token
            WHERE """)
            token_id = " id=%d" % int(token)
            find_tok += token_id
            r = self.__db.execute( text ( find_tok ) )
            tok_list = list(r)
            if len(tok_list)==0:
                self.__result['message']="Invalid token"
            else:
                self.__result['messsage']="Token Valid"
                self.__result['success']=True
        except Exception as e:
                self.__result['messsage']="Failed to find token!Reason:%s" % e
                
        return self.__result
        
class user():
    def __init__(self):
        self.__db = create_engine('mysql+pymysql://root:test@localhost/beyond_db', echo=True)
        self.__connection = self.__db.connect()
        self.__result = {'success':False, 'message':None, 'data':None}
        self.__metadata = MetaData(bind=self.__db)            
        self.__token_table = Table('token',self.__metadata,Column('id',Integer, primary_key=True, nullable=False),
                                   Column('admin_id', Integer, nullable=False),
                                   Column('date', Date(), nullable=False))
        self.__admin_table = Table('admin', self.__metadata,Column('id',Integer, primary_key=True, nullable=False),
                                   Column('username', String(20), nullable=False),
                                   Column('password', String(10),nullable=False))

    def check(self,data):
        try:
            date_now=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            s = select([self.__admin_table]).where(and_(self.__admin_table.c.username == data.get('username'), self.__admin_table.c.password == data.get('password')))
            r = self.__connection.execute(s)
            
            t = list(r)
            if len(t) == 0:
                self.__result['message']="Invalid Username/Password"
            else:
                self.__result['message']="Welcome:%s" % (t[0][1])
                self.__result['success']=True
                insert = self.__token_table.insert()
                new_token = insert.values(admin_id=t[0][0], date=date_now )
                
                #establish database connection
                insert_statement = self.__connection
                #execute insert statement
                insert_statement.execute(new_token)

                find_tok=("""SELECT * 
                FROM token
                WHERE """)
                admin_id = " admin_id=%d" % t[0][0]
                find_tok += admin_id
                
                r = self.__db.execute( text ( find_tok ) )
                tok_list = list(r)
                self.__result['data']=tok_list[0][0]
        
        except Exception as e:
            self.__result['message']="falied!%s" % e
        return self.__result

    def logout(self, id):
        try:
            remove_tok=("""DELETE 
            FROM token
            WHERE """)
            _id = " id=%d" % int(id.get('token_id'))
            remove_tok += _id
            
            self.__db.execute( text ( remove_tok ) )

            
            self.__result['message']="token deleted"
            self.__result['success']=True
        except Exception as e:
            self.__result['message']="falied to delete!Reason:%s" % e
            
        return self.__result


class hash_tag():
    def __init__(self):
        self.__db = create_engine('mysql+pymysql://root:test@localhost/beyond_db', echo=True)
        self.__connection = self.__db.connect()
        self.__result = {'success':False, 'message':None, 'data':None}
        self.__metadata = MetaData(bind=self.__db)
        self.__admin_table = Table('admin', self.__metadata,Column('id',Integer, primary_key=True, nullable=False),
                                   Column('username', String(20), nullable=False),
                                   Column('password', String(10),nullable=False))
        self.__admin_hashtags_table = Table('admin_hashtags',self.__metadata,Column('id',Integer, primary_key=True, nullable=False),
                                            Column('admin_id', Integer, nullable=False),
                                            Column('hashtag_id', Integer,nullable=False))
        self.__hashtag_table = Table('hashtag', self.__metadata,Column('id',Integer, primary_key=True, nullable=False),
                                                                  Column('hashtag', String(30), nullable=False),
                                                                  Column('date', Date(), nullable=False))
        self.__battle_table = Table('battle', self.__metadata,Column('id',Integer, primary_key=True, nullable=False),
                                Column('name', String(50), nullable=False),
                                Column('start_date', Date(), nullable=False),
                                Column('end_date', Date(), nullable=False),
                                Column('winner', String(30), nullable=False),
                                Column('incorrect_hash_tags', String(500), nullable=False),
                                Column('num_typos', String(30), nullable=False))

        self.__d = enchant.Dict("en_US")
    def get_battle(self):
        try:
            
            find_user = select([self.__admin_table])
            r = self.__connection.execute(find_user)
            user_list = list(r)
            hash_tags_init = hash_tag()
            get_hash_tag = hash_tags_init.get()
                    
            c = 0
            data = []
            typos = []
            num_typo = 0
            num_correct = 0
            users = {}
            user_1=0
            user_2=0
            user_1_typo=[]
            user_2_typo=[]
            
            while c < len(get_hash_tag.get('data')):
                d=get_hash_tag.get('data')
                tag = d[c].get('hash_tag')
                tag_frag = tag.split('#')
                check = self.__d.check(tag_frag[-1])
                user = d[c].get('user')
                user_list = list(users.values())
                users.update({user:user})
                if check == False:
                    num_typo += 1
                    typos.append({ 'hash_tag':tag_frag[-1], 'date':d[c].get('date'), 'user':user } )
                    if users.get('admin_1')==user:
                        user_1+=1
                    else:
                        user_2+=1

                c += 1

            d ={'user_1_num_typo':user_1,'user_2_num_typo':user_2 }
            self.__result['message']="Hash tags Found"
            self.__result['success']=True
            self.__result['data']=d#len(list(users.values()))
        except Exception as e:
            self.__result['message']="Failed!Reason:%s" % e
        return self.__result







    
    def create(self,data):
        try:
            # find_user = select([self.__admin_table])
            # r = self.__connection.execute(find_user)
            # user_list = list(r)
            # hash_tags_init = hash_tag()
            # get_hash_tag = hash_tags_init.get()
                    
            # c = 0
            # typos = []
            # user_1=0
            # user_2=0
            # while c < len(get_hash_tag.get('data')):
            #     d=get_hash_tag.get('data')
            #     tag = d[c].get('hash_tag')
            #     tag_frag = tag.split('#')
            #     check = self.__d.check(tag_frag[-1])
            #     user = d[c].get('user')
            #     user_list = list(users.values())
            #     users.update({user:user})
            #     if check == False:
            #         num_typo += 1
            #         typos.append({ 'hash_tag':tag_frag[-1], 'date':d[c].get('date'), 'user':user } )
            #         if users.get('admin_1')==user:
            #             user_1+=1
            #         else:
            #             user_2+=1

            #     c += 1

            # d ={'user_1_num_typo':user_1,'user_2_num_typo':user_2, 'typos_found':typos }
            # self.__result['message']="Battle Created"
            # self.__result['success']=True
            # self.__result['data']=d#len(list(users.values()))


            # insert = self.__battle_table.insert()
            # new_battle = insert.values(name=data.get('name'), start_date=data.get('start'), end_date=data.get('end') )
            
            # #establish database connection
            # insert_statement = self.__connection
            # #execute insert statement
            # insert_statement.execute(new_battle)

        except Exception as e:
            self.__result['message']="Failed!Reason:%s" % e


    def get(self):
        try:
            find_user = select([self.__admin_table])
            r = self.__connection.execute(find_user)
            user_list = list(r)
            if len(user_list)==0:
                self.__result['message']="No Hash Tag/s Found!"
            else:
                find_link = select([self.__admin_hashtags_table]).where(self.__admin_hashtags_table.c.admin_id == user_list[0][0])
                s = self.__connection.execute(find_link)
                links = list(s)
                counter = 0
                d = []
                while counter < len(links):
                    t = links[counter][2]
                    find_hash_tag = select([self.__hashtag_table]).where(self.__hashtag_table.c.id == t)
                    execute = self.__connection.execute(find_hash_tag)
                    data = list(execute)
                    d.append({ 'hash_tag':data[-1][1], 'date':datetime.datetime.strftime(data[-1][2],'%Y-%m-%d'), 'user':user_list[0][1] } )
                    counter += 1
                find_link_ = select([self.__admin_hashtags_table]).where(self.__admin_hashtags_table.c.admin_id == user_list[1][0])
                s_ = self.__connection.execute(find_link)
                links_ = list(s_)
                counter_ = 0
                while counter_ < len(links_):
                    t = links_[counter_][2]
                    find_hash_tag_ = select([self.__hashtag_table]).where(self.__hashtag_table.c.id == t)
                    execute_ = self.__connection.execute(find_hash_tag_)
                    data_ = list(execute_)
                    d.append({ 'hash_tag':data_[-1][1], 'date':datetime.datetime.strftime(data[-1][2],'%Y-%m-%d'), 'user':user_list[1][1] } )
                    counter_ += 1

                self.__result['message']="Hash tags Found"
                self.__result['success']=True
                self.__result['data']=d
        except Exception as e:
                self.__result['message']="Failed!Reason:%s" % e
                
        return self.__result
            
