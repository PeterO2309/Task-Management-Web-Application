from google.appengine.ext import ndb

class Task(ndb.Model):
    title = ndb.StringProperty()
    assigned_user = ndb.StringProperty()
    due_date = ndb.DateProperty()
    date_task_completed = ndb.StringProperty()
    time_task_completed = ndb.StringProperty()
    status = ndb.BooleanProperty()
    word_status = ndb.StringProperty()
    creator = ndb.StringProperty()

    #active_t = ndb.IntegerProperty()
    #completed_t = ndb.IntegerProperty()
    #total_t = ndb.IntegerProperty()
    #total_t_today = ndb.IntegerProperty()
