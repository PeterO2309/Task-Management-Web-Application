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


class Create(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        # pull the current user from the Request
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
        query = MyUser.query()


        template_values = {
            "user" : user,
            'url_string' : url_string,
            'url' : url,
        }


        # pull the template file and ask jinja to render
        # it with the given template values
        template = JINJA_ENVIRONMENT.get_template('create_taskboard.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        # pull the current user from the Request
        user = users.get_current_user()
        id = user.user_id()
        print(id)
        new_tbd_id = ''
        action = self.request.get('button')
        print("hey")
        print(id)

        name = self.request.get('tbd_name')

        if user and action == 'Submit':
            myuser_key = ndb.Key('MyUser', id)
            myuser = myuser_key.get()

            new_taskboard = TaskBoard()

            new_taskboard.tbd_name = self.request.get('tbd_name')
            #new_taskboard.tbd_creator = myuser_key
            new_taskboard.tbd_creator_email = user.email()

            new_taskboard.put()
            new_tbd_id = ndb.Key('TaskBoard', new_taskboard.key.id())
            myuser.tb_key.append(new_tbd_id)
            myuser.put()

            self.redirect('/view_taskboard')

        elif user and action == 'Cancel':
            self.redirect('/view_taskboard')
        else:
            self.redirect('/view_taskboard')
