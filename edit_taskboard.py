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


class EditTaskboard(webapp2.RequestHandler):
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

        id = user.user_id()
        myuser_key = ndb.Key('MyUser', id)
        myuser = myuser_key.get()

        #name = self.request.get('tbd_name')
        url_ID =long(self.request.get('ID'))

        tbd_id = ndb.Key('TaskBoard', url_ID)
        tb_clicked = tbd_id.get()


        tb_users_list = tb_clicked.tbd_users_email


        template_values = {
            'myuser' : myuser,
            'user' : user,
            'tb_clicked' : tb_clicked,
            'url_string' : url_string,
            'url' : url,
        }


        # pull the template file and ask jinja to render
        # it with the given template values
        template = JINJA_ENVIRONMENT.get_template('edit_taskboard.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'


        if (self.request.get('button') == 'Rename TB'):
            url_ID=self.request.get("ID")
            url_ID = long(url_ID)

            tbd_id = ndb.Key('TaskBoard', url_ID)
            tb_clicked = tbd_id.get()

            name = self.request.get("name")

            tb_clicked.tbd_name = name
            tb_clicked.put()
            message = 'name updated'
            self.redirect('/view_each_tb?ID=' + str(url_ID))

        elif (self.request.get('button') == 'Delete TB'):
            user = users.get_current_user()
            myuser_key = ndb.Key('MyUser', user.user_id())
            myuser = myuser_key.get()

            url_ID=self.request.get("ID")
            url_ID = long(url_ID)

            tbd_id = ndb.Key('TaskBoard', url_ID)
            tb_clicked = tbd_id.get()

            name = self.request.get("name")

            for i in tb_clicked.tk_key:
                t_id = ndb.Key('Task', i.id())
                t_obj = t_id.get()

                del t_obj.title
                del t_obj.assigned_user
                del t_obj.due_date
                del t_obj.date_task_completed
                del t_obj.status
                del t_obj.word_status
                del t_obj.creator
                #task_obj.put()

                #tb_clicked.tk_key.remove(t_id)
                #tb_clicked.put()

            del tb_clicked.tbd_name
            #del tb_clicked.tbd_creator
            del tb_clicked.tbd_creator_email
            #del tb_clicked.tbd_user[:]
            del tb_clicked.tk_key[:]

            # emptys the taskboard user email lists
            del tb_clicked.tbd_users_email[:]
            tb_clicked.put()

            myuser.tb_key.remove(tbd_id)

            logging.info("START")
            print(tb_clicked.tbd_users_email)
            print(tb_clicked.tk_key)
            logging.info("END")
            self.redirect('/view_each_tb?ID=' + str(url_ID))



        elif (self.request.get('button') == 'Remove user'):
            url_ID=self.request.get("ID")
            url_ID = long(url_ID)

            tbd_id = ndb.Key('TaskBoard', url_ID)
            tb_clicked = tbd_id.get()

            user_removed = self.request.get("remove")


            for i in tb_clicked.tk_key:
                #if user_removed in tb_clicked.tbd_users_email:
                if i.get().assigned_user == user_removed:
                    t_id = ndb.Key('Task', i.id())
                    t_obj = t_id.get()
                    t_obj.assigned_user = ''
                    t_obj.put()

            tb_clicked.tbd_users_email.remove(user_removed)

            tb_clicked.put()


            self.redirect('/view_each_tb?ID=' + str(url_ID))

        elif (self.request.get('button') == 'Cancel'):
            self.redirect('/view_taskboard')
        else:
            self.redirect('/view_taskboard')
