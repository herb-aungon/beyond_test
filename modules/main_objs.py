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
                                Column('num_typos', String(30), nullable=False))

        self.__d = enchant.Dict("en_US")
        
    def get_battle(self):
        try:
            battle="""SELECT * 
            FROM battle"""
                
            get = self.__db.execute( text ( battle ) )
            battle_list = list(get)
            
            self.__result['message']="Hash tags Found"
            self.__result['success']=True
            self.__result['data']=battle_list
        except Exception as e:
            self.__result['message']="Failed!Reason:%s" % e
        return self.__result


    def create(self,data):
        try:
            start = datetime.datetime.strptime(data.get('start'),'%Y-%m-%d')
            end = datetime.datetime.strptime(data.get('end'),'%Y-%m-%d')

            if start > end:
                self.__result['message']="Invalid duration for battle. Start date cannot be greater than End date"
            else:
                insert = self.__battle_table.insert()
                new_battle = insert.values(name=data.get('name'), start_date=data.get('start'), end_date=data.get('end') )
            
                #establish database connection
                insert_statement = self.__connection
                #execute insert statement
                insert_statement.execute(new_battle)
                self.__result['message']="Battle Created. Range from %s-%s" % (str(start),str(end))
                
            
        except Exception as e:
            self.__result['message']="Failed to create battle!Reason:%s" % e
            
        return self.__result


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
            
class battle():
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
                                Column('num_typos', String(30), nullable=False))

        self.__d = enchant.Dict("en_US")



    def update(self,data):
        try:
            start = datetime.datetime.strptime(data.get('start'),'%Y-%m-%d')
            end = datetime.datetime.strptime(data.get('end'),'%Y-%m-%d')

            if start > end:
                self.__result['message']="Invalid duration for battle. Start date cannot be greater than End date"
            else:

                #update battle table
                update_battle=self.__battle_table.update().\
                            where(self.__battle_table.c.name == data.get('name') ).\
                            values(start_date=start, end_date=end) 
                s = self.__connection.execute(update_battle)
                
                self.__result['message']="Battle Details for %s has been Updated" % data.get('name')
                self.__result['success']=True
        except Exception as e:
                self.__result['message']="Unable to update %s!Reason:%s" % (data.get('name'),e)
                
        return self.__result



    def delete_(self,data):
        try:
            name = data.get('name')
            if name==None:
                self.__result['message']="Unable to delete battle.Please check the name is correct"
            else:
                #update battle table
                delete_battle=self.__battle_table.delete().\
                            where(self.__battle_table.c.name == name )
                s = self.__connection.execute(delete_battle)
                self.__result['message']="Details for %s has been deleted" % name
                self.__result['success']=True
        except Exception as e:
            self.__result['message']="Unable to delete %s!Reason:%s" % (name,e)
                
        return self.__result

        
    def get(self,data):
        try:
            find_battle = select([self.__battle_table]).where(self.__battle_table.c.name == data.get('name') )
            s = self.__connection.execute(find_battle)
            battle_found = list(s)
            
            # r = self.__db.execute( text ( find_battle ) )
            # battle_found = list(r)
            self.__result['message']="Battle for %s has been returned" % data.get('name')
            self.__result['data']=battle_found
            self.__result['success']=True
        except Exception as e:
                self.__result['message']="Unable to find battle for %s!Reason:%s" % (data.get('name'),e)
                
        return self.__result
            
    def start(self,data):
        try:
            get_init = battle()
            get_battle = get_init.get(data)
            battle_info = get_battle.get('data')
            name = battle_info[0][1]
            start = battle_info[0][2]
            end = battle_info[0][3]
            
            find_hashtag = select([self.__hashtag_table]).where( between(self.__hashtag_table.c.date,start, end ))
            s = self.__connection.execute(find_hashtag)
            hashtag_found = list(s)
            num_hash = len(hashtag_found)

            #stores has tags in dictionary for easy access
            hash_dict={}
            hash_counter = 0

            while hash_counter < len(hashtag_found):
                hash_dict.update( { hashtag_found[hash_counter][0]:hashtag_found[hash_counter][1] } )
                hash_counter+=1
            
            if num_hash==0:
                self.__result['message']="No hashtags found!Please check daterange"
            else:
                #find the admin id
                user = select([self.__admin_table])
                find_user = self.__connection.execute(user)
                user_list = list(find_user)
                user_1 = {'id':user_list[0][0], 'name':user_list[0][1]}
                user_2 = {'id':user_list[1][0], 'name':user_list[1][1]}
                
                user = select([self.__admin_table])
                find_user = self.__connection.execute(user)
                user_list = list(find_user)

                #find tags link with admin
                user_id = [user_1.get('id'), user_2.get('id')]
                name=[user_1.get('name'),user_2.get('name')]
                user_c = 0
                tags_id=[]
                user_2_tags_id=[]
                t = []
                t2 = []
                typo_stats = {}
                typo_stats['hashtags_found']=hash_dict
                while user_c < len(user_id):
                    _id = user_id[user_c]
                    find_link = select([self.__admin_hashtags_table]).where(self.__admin_hashtags_table.c.admin_id==_id)
                    link = self.__connection.execute(find_link)

                    list_link=list(link)
                    
                    #stores the hash tags ids link for the admin
                    tag_ids =[]
                    tags_c = 0

                    while tags_c < len(list_link):
                        tag_ids.append(list_link[tags_c][2])
                        tags_c+=1
                        
                    typo = []
                    typo_c=0

                    #check for typo
                    while typo_c < len(tag_ids):
                        get_hash_val =  hash_dict.get(tag_ids[typo_c])
                        if get_hash_val != None:
                            hash_split =get_hash_val.split('#') 
                            check = self.__d.check(hash_split[-1])
                            if check == False:
                                typo.append(hash_split[-1])
                                t2.append(hash_split[-1])
                        typo_c+=1

                    typo_stats["%s_typos" % user_list[user_c][1]]=typo
                    typo_stats["%s_num_typos" % user_list[user_c][1]]=len(typo)
                    
                    user_c +=1

                #calculates the winner
                counter = 0
                cal_winner = []
                #calculate the winner
                while counter < len(user_id):
                    admin_name =user_list[counter][1]
                    loc = "%s_num_typos" % admin_name

                    cal_winner.append(typo_stats.get(loc))
                    #cal_winner.update({admin_name:typo_stats.get(loc)})
                    counter +=1
                if counter == len(user_id):
                    winner = min(cal_winner)
                #grabs the name of the winner
                name_winner_raw = list(typo_stats.keys())[list(typo_stats.values()).index(winner)]
                name_winner_frag = name_winner_raw.split('_')
                name_winner ="%s_%s" %(name_winner_frag[0], name_winner_frag[1])
                typo_stats["winner"]=name_winner

                typos_update ="%s_typos" % (name_winner)#ypo_stats.get("%s_typos") % (name_winner)

                #update battle table
                update_battle=self.__battle_table.update().\
                               where(self.__battle_table.c.name == data.get('name') ).\
                               values(winner=name_winner, num_typos=winner) #incorrect_hash_tags = tuple(typo_stats.get(typos_update)), 
                s = self.__connection.execute(update_battle)

                self.__result['s']=typos_update                
                self.__result['success']=True
                self.__result['message']="Battle Started and Finished"
                self.__result['data']=typo_stats
        except Exception as e:
                self.__result['message']="Failed to start battle!Reason:%s" % e
                
        return self.__result
