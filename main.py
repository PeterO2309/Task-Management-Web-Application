import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os
import logging


from myuser import MyUser
from create_taskboard import Create
from viewtaskboard import ViewTaskboard
from edit_taskboard import EditTaskboard
from view_each_tb import View
from view_task import ViewTask


# Setting up the environment for Jinja to work in as we construct a
# jinja2.Environment object.
JINJA_ENVIRONMENT = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        # URL that will contain a login or logout link
        # and also a string to represent this
        url = ''
        url_string = ''
        welcome = 'Welcome back'

        # pull the current user from the Request
        user = users.get_current_user()

        # determine if we have a user logged in or not
        if user:
            url = users.create_logout_url(self.request.uri)
            url_string = 'logout'

            myuser_key = ndb.Key('MyUser', user.user_id())
            myuser = myuser_key.get()

            if myuser == None:
                welcome = 'Welcome to the application'
                myuser = MyUser(id = user.user_id())
                myuser.email_address = user.email()
                myuser.put()


        else:
            url = users.create_login_url(self.request.uri)
            login_status = "You are not logged in."
            url_string = 'login'



        template_values = {
            'url' : url,
            'url_string' : url_string,
            'user' : user,
        }


            # pull the template file and ask jinja to render
            # it with the given template values
        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/create_taskboard', Create),
    ('/view_taskboard', ViewTaskboard),
    ('/edit_taskboard', EditTaskboard),
    ('/view_each_tb', View),
    ('/view_task', ViewTask),

], debug=True)
