from google.appengine.ext import ndb

from task import Task

class TaskBoard(ndb.Model):

    tbd_name = ndb.StringProperty()
    tk_key = ndb.KeyProperty(kind=Task, repeated = True)

    #tk_title_list = ndb.StringProperty(repeated = True)

    #tbd_creator = ndb.KeyProperty()
    tbd_creator_email = ndb.StringProperty()
    #tbd_users = ndb.KeyProperty(repeated = True)
    tbd_users_email = ndb.StringProperty(repeated = True)
