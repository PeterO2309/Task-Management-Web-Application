import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb

import os
import logging

from myuser import MyUser
from taskboard import TaskBoard
from task import Task
from datetime import datetime


# Setting up the environment for Jinja to work in as we construct a
# jinja2.Environment object.
JINJA_ENVIRONMENT = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class ViewTask(webapp2.RequestHandler):
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

        url_ID  =  self.request.get('tb_ID')
        url_ID = long(url_ID)
        t_ID=self.request.get("t_ID")
        t_ID=long(t_ID)
        index = int (self.request.get("index")) - 1

        myuser_key = ndb.Key('MyUser', id)
        myuser = myuser_key.get()

        tbd_id = ndb.Key('TaskBoard', url_ID)
        tb_clicked = tbd_id.get()

        task_obj = Task()
        for i in tb_clicked.tk_key:
            if i.get().key.id() == t_ID:
                task_obj = i.get()
                break


        template_values = {
            'tb_clicked' : tb_clicked,
            'task_obj' : task_obj,
            #'length' : length,
            'user' : user,
            'myuser' : myuser,
            'index' : index,
            'url_string' : url_string,
            'url' : url,
        }


        # pull the template file and ask jinja to render
        # it with the given template values
        template = JINJA_ENVIRONMENT.get_template('view_task.html')
        self.response.write(template.render(template_values))

    def post(self):
        action = self.request.get('button')


        if action == "Edit":
            url_ID=long(self.request.get('f_id'))
            t_ID=long(self.request.get("t_id"))

            index = int (self.request.get("index"))
            exist = 0
            unique = 0
            state = False
            state_word = "not completed"

            new_title =  self.request.get('title')
            new_assigned_user = self.request.get('assigned_user')
            new_due_date = self.request.get('due_date')
            hstripped_due_date = datetime.strptime(new_due_date, '%Y-%m-%d')

            new_status = self.request.get('status')

            datetimeobj = datetime.now()

            if new_status.lower() in ("yes", "true", "t", "1"):
                state = True
                state_word = "completed"
                date_tc = datetimeobj.strftime("%d-%m-%Y")
                time_tc = datetimeobj.strftime("%I:%M:%S %p")
            else:
                state = False
                state_word = "not completed"
                date_tc = ""
                time_tc = ""

            tbd_id = ndb.Key('TaskBoard', url_ID)
            tb_clicked = tbd_id.get()

            for i in tb_clicked.tk_key:
                if i.get().key.id() == t_ID:
                    task_obj = i.get()
                    break

            for i in tb_clicked.tk_key:
                if (i.get().title.lower() == new_title.lower()):
                    exist += 1 #Task already exist

            for i in tb_clicked.tk_key:
                if (i.get().title.lower() == new_title.lower() and
                    (t_ID == i.get().key.id())):
                    task_obj = i.get()
                    unique += 1 #Task already exist
                    break


                # If task object exists in the taskboard, check to see if task
                # with similar name already exists
            if(unique == 1):

                # Append values to the lists
                task_obj.title = new_title
                task_obj.assigned_user = new_assigned_user
                task_obj.due_date = hstripped_due_date
                task_obj.status  = state
                task_obj.word_status  = state_word
                task_obj.date_task_completed = date_tc
                task_obj.time_task_completed = time_tc

                task_obj.put()

                tkey = ndb.Key('Task', task_obj.key.id())
                new_t_obj = tkey.get()
                #tbd_obj.tk_title_list.append(new_task.title)
                #tb_clicked.tk_key.append(tkey)
                tb_clicked.put()
                message = 'Task details updated'
                self.redirect('/view_each_tb?ID=' + str(url_ID))

            elif(exist == 0):
                # Append values to the lists
                task_obj.title = new_title
                task_obj.assigned_user = new_assigned_user
                task_obj.due_date = hstripped_due_date
                task_obj.status = state
                task_obj.word_status  = state_word
                task_obj.date_task_completed = date_tc
                task_obj.time_task_completed = time_tc
                task_obj.put()

                tkey = ndb.Key('Task', task_obj.key.id())
                new_t_obj = tkey.get()
                #tbd_obj.tk_title_list.append(new_task.title)
                #tb_clicked.tk_key.append(tkey)
                tb_clicked.put()
                message = 'Task details updated'
                self.redirect('/view_each_tb?ID=' + str(url_ID))


            else:
                message = 'Task exists'
                self.redirect('/view_each_tb?ID=' + str(url_ID))
