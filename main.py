#!/usr/bin/env python                                                                                                                                                                                       
#-*- coding: utf-8 -*- 

from flask import Flask,request, render_template, flash, jsonify, make_response, Response, url_for, redirect
import json
from modules.main_objs import *
 
app = Flask(__name__)

"""
Flask config for changing Debug mode, SECRET_KEY
"""
app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='development key',
))


#Used to display errors on webpage
@app.errorhandler( 500 )
def internal_500_error( exception ):
     #app.logger.exception( exception )
     return json.dumps( exception )

@app.errorhandler( 404 )
def internal_404_error( exception ):
     #app.logger.exception( exception )
     return 'test page" <br/>\n%s<br/>\n%s' % ( exception, request.url )

@app.errorhandler( 401 )
def internal_401_error( exception ):
     #app.logger.exception( exception )
     return 'exercise page<br/>\n%s<br/>\n%s' % ( exception, request.url )


def default_encoder( obj, encoder=json.JSONEncoder() ):
     if isinstance(obj, datetime.datetime):
          date = datetime.date(obj.year, obj.month, obj.day)
          return str(date)#.strftime( '%Y-%m-%d' )
     return encoder.default( obj )
     
@app.route("/beyond_login", methods = [ 'GET' ] )
def login_get():
     return render_template('log_in.html')

@app.route("/beyond_login", methods = [ 'OPTIONS' ] )
def login_options():
     return ''


@app.route("/beyond_login", methods = [ 'POST' ] )
def login_post():
     try:
          payload = request.data
          payload_json = json.loads(payload)
          #resp.headers.add('X-token',token_id)
          user_init = user()
          user_check = user_init.check(payload_json)
          
          if user_check.get('success')==True:
               resp = json.dumps(user_check, default=default_encoder)
          else:
               message = user_check.get('message')
               flash(message)
               resp = json.dumps(user_check, default=default_encoder)
     except Exception as e:
          resp="Error! %s " % e
     return resp

@app.route("/home/<user>/<token_id>", methods = [ 'GET' ] )
def home_get(user,token_id):
     token_init = token()
     token_auth = token_init.token_validator(token_id)
     hash_tags=None
     if token_auth.get('success')==True:
          hash_tags_init = hash_tag() 
          get_hash_tags = hash_tags_init.get()
          
          if get_hash_tags.get('success')==True:
               hash_tags = get_hash_tags.get('data')
          else:
               message = json.dumps("Failed: %s" % get_hash_tags.get('message'))
               
          resp = render_template('start_battle.html', username= user, hash_tags=hash_tags, test =get_hash_tags)
     else:
          message = json.dumps("Failed: %s" % token_auth.get('message'))
          resp = redirect(url_for('login_get'))
          flash(message)
     return resp


@app.route("/home/<user>/<token_id>", methods = [ 'OPTIONS' ] )
def home_options():
     return ''
@app.route("/home/<user>/<token_id>/battle", methods = [ 'GET' ] )
def battle_get(user,token_id):
     token_init = token()
     token_auth = token_init.token_validator(token_id)
     hash_tags=None
     if token_auth.get('success')==True:
          try:
               battle_init = hash_tag()
               get_battle_ = battle_init.get_battle()
               if get_battle_.get('success')==True:
                    battle = get_battle_.get('data')
                    
               else:
                    message = json.dumps("Failed to load data: %s" % get_battle_.get('message'))
                    flash(message)
               resp = render_template('battle.html', test=get_battle_, battle=battle)

          except Exception as e:
               message="Error! %s " % e
               flash(message)
               resp = render_template('battle.html')
     else:
          message = json.dumps("Failed: %s" % token_auth.get('message'))
          resp = redirect(url_for('login_get'))
          flash(message)
     return resp

@app.route("/home/<user>/<token_id>/battle", methods = [ 'OPTIONS' ] )
def battle_options(user,token_id):
     return ''

@app.route("/home/<user>/<token_id>/battle", methods = [ 'POST' ] )
def battle_post(user,token_id):
     token_init = token()
     token_auth = token_init.token_validator(token_id)
     hash_tags=None
     if token_auth.get('success')==True:
          try:
               payload = request.data
               payload_json = json.loads(payload)
               create_battle_init = hash_tag()
               create_battle = create_battle_init.create(payload_json)
               resp = json.dumps(create_battle)

          except Exception as e:
               resp="Error! %s " % e
     else:
          if token_auth.get('message')==None:
               message = json.dumps("Token is not recognised!Please Log out!Reason:%s" % token_auth.get('message'))
          else:
               message = json.dumps("Failed!Please Log out!Reason: %s" % token_auth.get('message'))
          #resp = redirect(url_for('login_get'))
          resp=message
          flash(message)
     return resp



@app.route("/home/<user>/<token_id>/battle/manage", methods = [ 'GET' ] )
def manage_battle_get(user,token_id):
     return ''


@app.route("/home/<user>/<token_id>/battle/manage", methods = [ 'POST' ] )
def manage_battle_post(user,token_id):
     token_init = token()
     token_auth = token_init.token_validator(token_id)
     hash_tags=None
     if token_auth.get('success')==True:
          try:
               payload = request.data
               payload_json = json.loads(payload)
               start_init = battle()
               start_battle = start_init.start(payload_json)
               result = json.dumps(start_battle)
               
               resp = result #render_template('battle.html', test=test, battle=None)

          except Exception as e:
               resp="Error! %s " % e
     else:
          if token_auth.get('message')==None:
               message = json.dumps("Token is not recognised!Please Log out!Reason:%s" % token_auth.get('message'))
          else:
               message = json.dumps("Failed!Please Log out!Reason: %s" % token_auth.get('message'))
          #resp = redirect(url_for('login_get'))
          resp=message
          flash(message)
     return resp

@app.route("/home/<user>/<token_id>/battle/manage", methods = [ 'PUT' ] )
def manage_battle_put(user,token_id):
     token_init = token()
     token_auth = token_init.token_validator(token_id)
     if token_auth.get('success')==True:
          try:
               payload = request.data
               payload_json = json.loads(payload)
               update_init = battle()
               update_battle = update_init.update(payload_json)
               result = json.dumps(update_battle)
               
               resp = result #render_template('battle.html', test=test, battle=None)

          except Exception as e:
               resp="Error! %s " % e
     else:
          if token_auth.get('message')==None:
               message = json.dumps("Token is not recognised!Please Log out!Reason:%s" % token_auth.get('message'))
          else:
               message = json.dumps("Failed!Please Log out!Reason: %s" % token_auth.get('message'))
          #resp = redirect(url_for('login_get'))
          resp=message
          flash(message)
     return resp


@app.route("/home/<user>/<token_id>/battle/manage", methods = [ 'DELETE' ] )
def manage_battle_del(user,token_id):
     token_init = token()
     token_auth = token_init.token_validator(token_id)
     if token_auth.get('success')==True:
          try:
               payload = request.data
               payload_json = json.loads(payload)
               del_init = battle()
               del_battle = del_init.delete_(payload_json)
               result = json.dumps(del_battle)
               
               resp = result #render_template('battle.html', test=test, battle=None)

          except Exception as e:
               resp="Error! %s " % e
     else:
          if token_auth.get('message')==None:
               message = json.dumps("Token is not recognised!Please Log out!Reason:%s" % token_auth.get('message'))
          else:
               message = json.dumps("Failed!Please Log out!Reason: %s" % token_auth.get('message'))
          #resp = redirect(url_for('login_get'))
          resp=message
          flash(message)
     return resp


@app.route("/home/<user>/<token_id>/battle/manage", methods = [ 'OPTIONS' ] )
def manage_battle_opts(user,token_id):
     return ''



@app.route("/logout", methods = [ 'DELETE' ] )
def logout_del():
     try:
          payload = request.data
          payload_json = json.loads(payload)
          user_init = user()
          user_check = user_init.logout(payload_json)
          if user_check.get('success')==True:
               resp = json.dumps(user_check, default=default_encoder)
          else:
               message = user_check.get('message')
               flash(message)
               resp = json.dumps(user_check, default=default_encoder)
     except Exception as e:
          resp="Error! %s " % e
     return resp


@app.route("/logout", methods = [ 'OPTIONS' ] )
def logout_opts():
     return ''


if __name__ == "__main__":
    app.run(debug=True)
    #app.run()
