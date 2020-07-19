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


class View(webapp2.RequestHandler):
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
        tb_clicked = ''
        tb_name_clicked = ""
        tb_name_clicked_inv = ""
        tb_key_clicked = []
        tb_users_email_clicked = []
        tb_users_email_clicked_inv = []
        total_users_incl_creator = []
        title_list = []
        assigned_user_list = []
        duedate_list = []
        status_list = []
        state = -1
        task_status = []
        #message = ''

        myuser_key = ndb.Key('MyUser', id)
        myuser = myuser_key.get()

        #name = self.request.get('tbd_name')
        url_ID =long(self.request.get('ID'))
        #print(name)
        print(url_ID)
        logging.info("EFF")

        #queries the datastore for all users except the creator
        all_users = MyUser.query(ndb.AND(MyUser.email_address != myuser.email_address))
        #all_users = MyUser.query()
        query = MyUser.query().fetch(keys_only=True)
        for i in query:
            total_users_incl_creator.append(i.get().email_address)
            print(total_users_incl_creator)


        tbd_id = ndb.Key('TaskBoard', url_ID)
        tb_clicked = tbd_id.get()

        #if tb_clicked == None:
            #tb_clicked = TaskBoard()
            #tb_clicked.put()

        #if (myuser.email_address == i.get().tbd_creator_email):
        #tb_name_clicked = tb_clicked.tbd_name
        #tk_key_clicked = tb_clicked.tk_key
        tb_users_email_clicked = tb_clicked.tbd_users_email


        # getting the task ID from the form
        #t_ID=self.request.get("t_id")
        #t_ID=long(t_ID)

        #t_id = ndb.Key('TaskBoard', t_ID)
        #task_clicked = tbd_id.get()

        length = 0
        completedtaskcount=0
        activetasks=0
        completedtoday = 0
        totaltask = 0
        datetimeobj = datetime.now()
        dtime= datetimeobj.strftime("%d-%m-%Y")
        #i.get().date_task_completed = datetimeobj.strftime("%d-%b-%Y (%H:%M:%S)")


        #if (len(tb_clicked.tk_key) != 0):
        for i in tb_clicked.tk_key:
            task_id = ndb.Key('Task', i.id())
            task_obj = task_id.get()

            #logging.info("HEY")
            #print(task_obj.status)
            if task_obj.status==True:
                completedtaskcount=completedtaskcount+1

                if i.get().date_task_completed == dtime:
                    completedtoday=completedtoday+1
            if task_obj.status==False:
                activetasks=activetasks+1

        totaltask = completedtaskcount + activetasks


        template_values = {
            'tb_clicked' : tb_clicked,
            #'task_obj' : task_obj,
            'length' : length,
            'url_string' : url_string,
            'url' : url,
            'completedcount':completedtaskcount,
            'activetasks':activetasks,
            'totaltask' : totaltask,
            'completedtoday' : completedtoday,
            #'message' : message,

            #'task_clicked' : task_clicked,
            'user' : user,
            'myuser' : myuser,
            'all_users' : all_users,
            #'tb_name_clicked' : tb_name_clicked,
            #'tb_name_clicked_inv' : tb_name_clicked_inv,
            'users_list' : tb_users_email_clicked,
            #'users_list_inv' : tb_users_email_clicked_inv,
            #'tasks_list' : tb_clicked.tk_key,
            #'duedate_list' : duedate_list,
            #'title_list' : title_list,
            #'assigned_user_list' : assigned_user_list,
            #'status_list' : status_list,
            #'status' : task_status,
        }


        # pull the template file and ask jinja to render
        # it with the given template values
        template = JINJA_ENVIRONMENT.get_template('view_each_tb.html')
        self.response.write(template.render(template_values))


    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        query = MyUser.query()
        tb_invited_users_list = []
        user = users.get_current_user()
        id = user.user_id()
        myuser_key = ndb.Key('MyUser', id)
        myuser = myuser_key.get()
        message = ''

        all_users = MyUser.query(ndb.AND(MyUser.email_address != myuser.email_address))


        if (self.request.get('button') == 'Invite users'):
            url_ID=self.request.get("f_id")
            url_ID = long(url_ID)
            #logging.info("HEY")
            #print(url_ID)
            #logging.info("YEE")


            name = self.request.get('tbd_name')

            # For the selected user,add the TB key to the invited TB list
            selected = self.request.get('invite')
            selected_user = ndb.Key('MyUser',selected)
            selected_user_obj = selected_user.get()
            #logging.info("MNX")
            #print(type(i.get().key.id()))
            #print(i.get().key.id())
            #print(type(url_ID))
            #print(url_ID)
            #print(url_ID == i.id())
            #logging.info("END")

            # For the current user/ creator of the taskboard
            adduser_key = ndb.Key('TaskBoard', url_ID)
            adduser_obj = adduser_key.get()

            if (myuser.email_address == adduser_obj.tbd_creator_email):
                #When inviting a new user to the TB, check if the User and the TB creator is in the TB members' list
                if (selected_user.get().email_address not in adduser_obj.tbd_users_email ):
                    if (adduser_obj.tbd_creator_email not in adduser_obj.tbd_users_email ):
                        adduser_obj.tbd_users_email.append(adduser_obj.tbd_creator_email)
                        #adduser_obj.tbd_users.append(myuser_key)

                    else:
                        print("Do nothing")

                    adduser_obj.tbd_users_email.append(selected_user.get().email_address)
                    #selected_user_obj.tb_key.append(adduser_key )

                    selected_user_obj.put()
                    adduser_obj.put()
                    message = 'New user added to the taskboard'

                    #self.redirect('/view_each_tb?tbd_name=' + name)

                else:
                    message = 'User already exists in the Taskboard'
                self.redirect('/view_each_tb?ID=' + str(url_ID))
            else:
                #logging.info("Start message 1")
                #print('Only the creator can invite users')
                #logging.info("Debug message 2")
                message = 'Only the creator can invite users'
                self.redirect('/view_each_tb?tbd_name=' + name)

        elif  self.request.get('button') == 'Add a task':

            url_ID=self.request.get("f_id")
            url_ID=long(url_ID)

            exist = 0

            task_obj = Task()

            tbd_key = ndb.Key('TaskBoard', url_ID)
            tbd_obj = tbd_key.get()
            mtitle = self.request.get('title')


            #for i in tbd_obj.tk_key:
                #task_id = ndb.Key('Task', i.id())
                #task_obj = task_id.get()

            for i in tbd_obj.tk_key:
                if i.get().title.lower() == mtitle.lower():
                    exist += 1 #Task already exist

            #if task_obj == None:
                #task_obj = Task()
                #task_obj.put()


            # If task object exists in the taskboard, check to see if task
            # with similar name already exists
            if(exist == 0):
                # Task doesnt exist
                htitle = self.request.get('title')
                hassigned_user = self.request.get('assigned_user')
                due_date = self.request.get('due_date')
                hstripped_due_date = datetime.strptime(due_date, '%Y-%m-%d')

                hcreator = myuser.email_address
                hstatus = False #a new task is defaulted to not complete


                # Append values to the lists
                task_obj.title = htitle
                task_obj.assigned_user =hassigned_user
                task_obj.due_date = hstripped_due_date
                task_obj.creator = hcreator
                task_obj.status = hstatus
                task_obj.word_status = "not completed"

                #task_obj.total_t += 1
                #task_obj.active_t += 1


                task_obj.put()

                tkey = ndb.Key('Task', task_obj.key.id())
                task_obj = tkey.get()
                tbd_obj.tk_key.append(tkey)
                tbd_obj.put()
                message = 'New%20Task%20added'
                self.redirect('/view_each_tb?ID=' + str(url_ID))



            else:
                message = 'Task already exists'
                self.redirect('/view_each_tb?ID=' + str(url_ID))

        elif  self.request.get('button') == 'not completed':
            logging.info(self.request.get('button'))
            url_ID=self.request.get("f_id")
            url_ID=long(url_ID)
            t_ID=self.request.get("t_id")
            t_ID=long(t_ID)
            exist = 0

            index = int(self.request.get('index')) - 1

            #ind = int (self.request.get("ind"))

            tbd_key = ndb.Key('TaskBoard', url_ID)
            tbd_obj = tbd_key.get()

            task_obj = Task()
            for i in tbd_obj.tk_key:
                if i.get().key.id() == t_ID:
                    datetimeobj = datetime.now()
                    task_obj = i.get()
                    i.get().status = True
                    i.get().word_status = "completed"
                    i.get().date_task_completed = datetimeobj.strftime("%d-%m-%Y")
                    i.get().time_task_completed = datetimeobj.strftime("%I:%M:%S %p")
                    task_obj.put()
                    break

            #self.redirect('/')
            self.redirect('/view_each_tb?ID=' + str(url_ID))

        elif  self.request.get('button') == 'completed':
            url_ID=self.request.get("f_id")
            url_ID=long(url_ID)
            t_ID=self.request.get("t_id")
            t_ID=long(t_ID)

            index = int(self.request.get('index')) - 1

            #ind = int (self.request.get("ind"))

            tbd_key = ndb.Key('TaskBoard', url_ID)
            tbd_obj = tbd_key.get()

            task_obj = Task()
            for i in tbd_obj.tk_key:
                if i.get().key.id() == t_ID:
                    task_obj = i.get()
                    i.get().status = False
                    i.get().word_status = "not completed"
                    i.get().date_task_completed = ""
                    i.get().time_task_completed = ""
                    task_obj.put()
                    break

            #self.redirect('/')
            self.redirect('/view_each_tb?ID=' + str(url_ID))

        elif  self.request.get('button') == 'Delete':
            url_ID=self.request.get("f_id")
            url_ID=long(url_ID)
            t_ID=self.request.get("t_id")
            t_ID=long(t_ID)

            index = int(self.request.get('index')) - 1

            #ind = int (self.request.get("ind"))

            tbd_key = ndb.Key('TaskBoard', url_ID)
            tbd_obj = tbd_key.get()


            task_key = ndb.Key('Task', t_ID)
            task_obj = task_key.get()

            del task_obj.title
            del task_obj.assigned_user
            del task_obj.due_date
            del task_obj.date_task_completed
            del task_obj.time_task_completed
            del task_obj.status
            del task_obj.word_status
            del task_obj.creator
            #task_obj.put()

            tbd_obj.tk_key.remove(task_key)


            tbd_obj.put()

            message = "Task deleted"

            self.redirect('/view_each_tb?ID=' + str(url_ID))

        else:
            self.redirect('/view_each_tb?ID=' + str(url_ID))
