from header import *
class Users(ndb.Model):
    username = ndb.StringProperty(default='')
    password = ndb.StringProperty(default='')
    firstname = ndb.StringProperty(default='')
    lastname = ndb.StringProperty(default='')
    fullname = ndb.StringProperty(default='')
    phone = ndb.StringProperty(default='')
    email = ndb.StringProperty(default='')
    tutor = ndb.BooleanProperty(default=False)
    aboutme = ndb.TextProperty()
    avatar = ndb.BlobKeyProperty()
    graduate = ndb.BooleanProperty(default=False)
    year = ndb.IntegerProperty() #1 = fresh, 2 = soph, 3 = junior, 4 = senior
    wepayuid = ndb.StringProperty(default='') #default sets it to empty
    wepayat = ndb.StringProperty(default='') #default sets it to empty
    major1 = ndb.StringProperty(default='')
    major2 = ndb.StringProperty(default='')
    major3 = ndb.StringProperty(default='')
    minor1 = ndb.StringProperty(default='')
    minor2 = ndb.StringProperty(default='')
    minor3 = ndb.StringProperty(default='')
    appliedastutor = ndb.BooleanProperty(default=False)
    admin = ndb.BooleanProperty(default=False)
    tos = ndb.BooleanProperty(default=False)
    available = ndb.BooleanProperty(default='False') #false if this user does not want to appear in searches.
    studentgroupname = ndb.StringProperty(default='') #if empty, this user is NOT a student group.

class Classes(ndb.Model):
    department = ndb.StringProperty()
    coursenumber = ndb.IntegerProperty()
    classname = ndb.StringProperty()
    active = ndb.BooleanProperty()
    semester = ndb.IntegerProperty()
    year = ndb.IntegerProperty() #Academic or Calendar?

class StudentClasses(ndb.Model):
    class_id = ndb.IntegerProperty()
    student = ndb.IntegerProperty()
    status = ndb.IntegerProperty() #0 for not looking, #1 for looking, #2 for found

class TutorClasses(ndb.Model):
    class_id = ndb.IntegerProperty()
    tutor = ndb.IntegerProperty()
    rate = ndb.FloatProperty()
    approved = ndb.BooleanProperty(default =False)

class Availabilities(ndb.Model):
    user = ndb.IntegerProperty()
    dayofweek = ndb.IntegerProperty()
    start = ndb.TimeProperty()
    end = ndb.TimeProperty()

class Departments(ndb.Model):
    code = ndb.StringProperty()
    name = ndb.StringProperty()

class Requests(ndb.Model):
    tutorclassid = ndb.IntegerProperty()
    student = ndb.IntegerProperty()
    notes = ndb.StringProperty()

class RequestLines(ndb.Model):
    requestid = ndb.IntegerProperty()
    start = ndb.DateTimeProperty()
    end = ndb.DateTimeProperty()
    cost = ndb.FloatProperty()

class Requesttotutor(ndb.Model):
    requestid = ndb.IntegerProperty()

class Appointments(ndb.Model):
    tutorclassid = ndb.IntegerProperty()
    student = ndb.IntegerProperty()
    start = ndb.DateTimeProperty()
    end = ndb.DateTimeProperty()
    cost = ndb.FloatProperty()
    paid = ndb.BooleanProperty()
    studentgroupname = ndb.StringProperty(default='') #if empty, the student will be paying instead.
    checkoutid = ndb.IntegerProperty(default=0) #checkout id in order to refund

class Settings(ndb.Model):
    logo = ndb.BlobKeyProperty()
    emblem = ndb.BlobKeyProperty()
    allowratings = ndb.BooleanProperty()
    tutorsetrate = ndb.BooleanProperty()
    tutorrate = ndb.FloatProperty()


class Resources(ndb.Model):
    html = ndb.StringProperty()
    order = ndb.IntegerProperty()

class StudentGroupRequests(ndb.Model):
    student = ndb.IntegerProperty() #links to User
    groupname = ndb.StringProperty(default='') #links to User.studentgroupname

class StudentGroups (ndb.Model):
    student = ndb.IntegerProperty() #links to User
    groupname = ndb.StringProperty(default='') #links to User.studentgroupnamez

def getUser(username,password):
    if not(username):
        return None
    users = Users.query(Users.username == username)
    user = None
    for x in users:
        user = x
    if not(user.password == hashlib.sha224(password).hexdigest()):
        return None
    return user

def getUserNoPassword(username):
    if not(username):
        return None
    users = Users.query(Users.username == username)
    for user in users:
        return user
    return None

def getDepartmentSelect():
    depts = Departments.query()
    depts = depts.order(Departments.code)
    string = ''
    for dept in depts:
        string+="<option>"+dept.code+"</option>"
    return string

#Options
#   Number of Semesters
#   Names of Semesters
#   Academic or Calendar Year?
#   Time Zone
BATCH_SIZE = 10 # ideal batch size may vary based on entity size.

def UpdateSchema(cursor=None, num_updated=0):

    time =Settings.query()
    a, cur, more =time.fetch_page(10)
    if cursor:
       # query.fetch_page(BATCH_SIZE, start_cursor=cursor)
        time.fetch_page(BATCH_SIZE, start_cursor=cursor)

    to_put = []
    for p in time:
        # In this example, the default values of 0 for num_votes and avg_rating
        # are acceptable, so we don't need this loop.  If we wanted to manually
        # manipulate property values, it might go something like this:
        #Users.aboutme = 'iwin'
        p.tutorrate=10;
        to_put.append(p)
        #query.put()

    if to_put:
        ndb.put_multi(to_put)
        #ndb.delete_multi([m.mamadouisawsome for m in
  #query])
        num_updated += len(to_put)
        logging.debug(
            'Put %d entities to Datastore for a total of %d',
            len(to_put), num_updated)
        deferred.defer(
            UpdateSchema, cursor=time.fetch_page(BATCH_SIZE), num_updated=num_updated)
    else:
        logging.debug(
            'UpdateSchema complete with %d updates!', num_updated)
