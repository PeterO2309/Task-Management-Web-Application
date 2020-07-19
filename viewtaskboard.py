import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb

import os
import logging

from myuser import MyUser
from taskboard import TaskBoard

# Setting up the environment for Jinja to work in as we construct a
# jinja2.Environment object.
JINJA_ENVIRONMENT = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class ViewTaskboard(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        # pull the current user from the Request
        user = users.get_current_user()
        tb_list = []
        tb_id_list = []
        tb_userslist = []
        invited_list = []

        user = users.get_current_user()

        if user == None:
            url_string = 'login'
            url = users.create_login_url(self.request.uri)
            template_values = {
                'url_string' : url_string,
                'url' : url,
                'login_url' : users.create_login_url(self.request.uri)
            }


            template = JINJA_ENVIRONMENT.get_template('main.html')
            self.response.write(template.render(template_values))
            return

        url_string = 'logout'
        url = users.create_logout_url(self.request.uri)

        id = user.user_id()
        myuser_key = ndb.Key('MyUser', id)
        myuser = myuser_key.get()

        print(myuser.tb_key)

        for n in myuser.tb_key:
            tboard = n.get()
            #if tboard == None:
                #tboard = TaskBoard()
                #tboard.put()

            logging.info("Debug message")
            print(n)
            logging.info("END")

            #tb_list.append(tboard)
            #tb_id_list.append(tboard.key.id())

        query = MyUser.query(ndb.AND(MyUser.email_address != myuser.email_address))

        #for n in query:
            #logging.info("START message")
            #print(n.email_address)
            #logging.info("End message")

        #for n in myuser.tb_key:
            #logging.info("Debug message")
            #print(n.get().tbd_name)
            #logging.info("END")
            #tb_userslist.append(n.get().tbd_name)

        #for n in myuser.invited_tb_list:
            #TaskBoard = n.get()
            #invited_list.append(TaskBoard)
            #invited_list.append(n.get().tbd_name)

        template_values = {
            'myuser' : myuser,
            'user' : user,
            #'tb_list' : tb_list,
            #'tboard' : tboard,
            'url_string' : url_string,
            'url' : url,
        }


        # pull the template file and ask jinja to render
        # it with the given template values
        template = JINJA_ENVIRONMENT.get_template('viewtaskboard.html')
        self.response.write(template.render(template_values))
