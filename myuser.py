from google.appengine.ext import ndb

from taskboard import TaskBoard

class MyUser(ndb.Model):
    # email address of this user
    email_address = ndb.StringProperty()
    #tb_name = ndb.StringProperty()
    tb_key = ndb.KeyProperty(repeated = True, kind=TaskBoard)
    invited_tb_list = ndb.KeyProperty(repeated = True, kind=TaskBoard)
