#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# diingibuted under the License is distringibuted on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


from header import *
import model
import au
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'])

# application settings
account_id = 860764059     # your app's account_id
access_token = 'PRODUCTION_7d635086b74e2bb90d8a13c0046bee6adba703b362d06e27645a12a5da553d59' # your app's access_token

client_id =147330
client_secret ="75d19ee2f1"

production = True
# set production to True for live environments
wepay = au.WePay(production, access_token)

class GeneralSettings(webapp2.RequestHandler):
    def get(self):
        settings = ndb.gql("select * from Settings")
        for item in settings:
                settings = item
        user = model.getUser(self.request.cookies.get('user',''),self.request.cookies.get('pass',''))
        date = datetime.now()
        if not(user):
            self.redirect('/')
            return
        if not(user.admin):
            self.redirect('/calendar.html')
            return
        classlist = ''
        deps = ndb.gql("SELECT * FROM Departments order by name")
        for dep in deps:
            classlist += '<li><a href="#">'+dep.name+'</a>'
            classlist2 = ''
            classes = ndb.gql("SELECT * FROM Classes where department = '"+dep.code+"'")
            for myclass in classes:
                classlist2 += '<li>'+dep.code+str(myclass.coursenumber)+': '+myclass.classname+'</li>'
            if classlist2 != '':
                classlist += '<ul>'+classlist2+'</ul>'
            classlist += '</li>'
        template_values = {
            'logo': au.getLogo(),
            'emblem': au.getEmblem(),
            'tab1': 'General Settings',
            'tab1url': '/gensettings.html',
            'tab2': 'Manage Tutors',
            'tab2url': '/managetutors.html',
            'tab3': 'Student Groups',
            'tab3url': '/gensettings.html',
            'tab4': 'Manage Resources',
            'tab4url': '/adminresources.html',
            'rate': settings.tutorrate,
            'time':str(date.date()),
             'checked':au.printstudentsetrate(settings),
            'classes': classlist,
        }
        template = JINJA_ENVIRONMENT.get_template('gensettings.html')
        self.response.write(template.render(template_values))

class AdminResources(webapp2.RequestHandler):
    def get(self):
        user = model.getUser(self.request.cookies.get('user',''),self.request.cookies.get('pass',''))
        if not(user):
            self.redirect('/')
            return
        if not(user.admin):
            self.redirect('/calendar.html')
            return
        classlist = ''
        deps = ndb.gql("SELECT * FROM Departments order by name")
        for dep in deps:
            classlist += '<li><a href="#">'+dep.name+'</a>'
            classlist2 = ''
            classes = ndb.gql("SELECT * FROM Classes where department = '"+dep.code+"'")
            for myclass in classes:
                classlist2 += '<li>'+dep.code+str(myclass.coursenumber)+': '+myclass.classname+'</li>'
            if classlist2 != '':
                classlist += '<ul>'+classlist2+'</ul>'
            classlist += '</li>'
        resources = ''
        resourcelist = ndb.gql("SELECT * FROM Resources ORDER BY order")
        for resource in resourcelist:
            resources += resource.html
        template_values = {
            'logo': au.getLogo(),
            'emblem': au.getEmblem(),
            'tab1': 'General Settings',
            'tab1url': '/gensettings.html',
            'tab2': 'Manage Tutors',
            'tab2url': '/gensettings.html',
            'tab3': 'Student Groups',
            'tab3url': '/gensettings.html',
            'tab4': 'Manage Resources',
            'tab4url': '/adminresources.html',
            'classes': classlist,
            'resources': resources
        }
        template = JINJA_ENVIRONMENT.get_template('adminresources.html')
        self.response.write(template.render(template_values))
        
class GroupCalendar(webapp2.RequestHandler):
    def get(self):
        user = model.getUser(self.request.cookies.get('user',''),self.request.cookies.get('pass',''))
        if not(user):
            self.redirect('/')
            return
        if user.admin:
            self.redirect('/gensettings.html')
            return
        if not(user.studentgroupname):
            self.redirect('/calendar.html')
            return
        template_values = {
            'logo': au.getLogo(),
            'emblem': au.getEmblem(),
            'calendar': '',
            'tab1': 'My Calendar',
            'tab1url': '/groupcalendar.html',
            'tab2': 'My Students',
            'tab2url': '/mystudents.html',
            'tab3': 'Payment Requests',
            'tab3url': '/paymentrequest.html',
            'tab4': 'Contact Us',
            'tab4url': '/contactus.html'
        }
        template = JINJA_ENVIRONMENT.get_template('calendar.html')
        self.response.write(template.render(template_values))
class contactus (webapp2.RequestHandler):
    def get(self):
        user = model.getUser(self.request.cookies.get('user',''),self.request.cookies.get('pass',''))
        if not(user):
            self.redirect('/')
            return
        if user.admin:
            self.redirect('/gensettings.html')
            return
        if not(user.studentgroupname):
            self.redirect('/calendar.html')
            return
        template_values = {
            'logo': au.getLogo(),
            'emblem': au.getEmblem(),
            'calendar': '',
            'tab1': 'My Calendar',
            'tab1url': '/groupcalendar.html',
            'tab2': 'My Students',
            'tab2url': '/mystudents.html',
            'tab3': 'Payment Requests',
            'tab3url': '/paymentrequest.html',
            'tab4': 'Contact Us',
            'tab4url': '/contactus.html'
        }
        template = JINJA_ENVIRONMENT.get_template('contact.html')
        self.response.write(template.render(template_values))
class sendmail(webapp2.RequestHandler):
    def post(self):
        user = model.getUser(self.request.cookies.get('user',''),self.request.cookies.get('pass',''))
        if not(user):
            self.redirect('/')
            return
        au.sendmessage(user.email,user.fullname,self.request.get("message"))
class MyStudents(webapp2.RequestHandler):
    def get(self):
        user = model.getUser(self.request.cookies.get('user',''),self.request.cookies.get('pass',''))
        if not(user):
            self.redirect('/')
            return
        if user.admin:
            self.redirect('/gensettings.html')
            return
        if not(user.studentgroupname):
            self.redirect('/calendar.html')
            return
        requeststring = ''
        requests = ndb.gql("SELECT * FROM StudentGroupRequests WHERE groupname = '"+user.studentgroupname+"'")
        for request in requests:
            requeststring += au.getStudentGroupRequestForm(request)
        studentstring = ''
        students = ndb.gql("SELECT * FROM StudentGroups WHERE groupname = '"+user.studentgroupname+"'")
        for studentgroup in students:
            student = model.Users.get_by_id(studentgroup.student)
            studentstring +='<tr><td class="info_fields">'
            studentstring +='<span>Student Name:&nbsp;&nbsp;<span style="color:#0093e7;">'+student.fullname+'</span>&nbsp;&nbsp;|'
            studentstring += '&nbsp;&nbsp;Student Email:&nbsp;&nbsp;<span style="color:#0093e7;">'+student.email+'</span></span></td></tr>'
        template_values = {
            'logo': au.getLogo(),
            'emblem': au.getEmblem(),
            'requests': requeststring,
            'students': studentstring,
            'groupname':str(user.studentgroupname),
            'tab1': 'My Calendar',
            'tab1url': '/groupcalendar.html',
            'tab2': 'My Students',
            'tab2url': '/mystudents.html',
            'tab3': 'Payment Requests',
            'tab3url': '/paymentrequest.html',
            'tab4': 'Contact Us',
            'tab4url': '/contactus.html'
        }
        template = JINJA_ENVIRONMENT.get_template('mystudents.html')
        self.response.write(template.render(template_values))

class AcceptStudent(webapp2.RequestHandler):
    def post(self):
        user = model.getUser(self.request.cookies.get('user',''),self.request.cookies.get('pass',''))
        if not(user):
            self.redirect('/')
            return
        if user.admin:
            self.redirect('/gensettings.html')
            return
        if not(user.studentgroupname):
            self.redirect('/calendar.html')
            return
        request = model.StudentGroupRequests.get_by_id(int(self.request.get('id')))
        studentgroup = model.StudentGroups(
            student = request.student,
            groupname = request.groupname)
        studentgroup.put()
        request.key.delete()
        time.sleep(.5)
        self.redirect('/mystudents.html')

class PaymentRequest(webapp2.RequestHandler):
    def get(self):
        user = model.getUser(self.request.cookies.get('user',''),self.request.cookies.get('pass',''))
        if not(user):
            self.redirect('/')
            return
        if user.admin:
            self.redirect('/gensettings.html')
            return
        if not(user.studentgroupname):
            self.redirect('/calendar.html')
            return
        appts = ndb.gql("SELECT * FROM Appointments WHERE studentgroupname = '"+user.studentgroupname+"'")
        apptstring = ''
        for appt in appts:
            apptstring += au.getGroupAppointmentInfo(appt)
        template_values = {
            'logo': au.getLogo(),
            'emblem': au.getEmblem(),
            'appointments': apptstring,
            'tab1': 'My Calendar',
            'tab1url': '/groupcalendar.html',
            'tab2': 'My Students',
            'tab2url': '/mystudents.html',
            'tab3': 'Payment Requests',
            'tab3url': '/paymentrequest.html',
            'tab4': 'Contact Us',
            'tab4url': '/contactus.html'
        }
        template = JINJA_ENVIRONMENT.get_template('paymentrequest.html')
        self.response.write(template.render(template_values))

class Calendar(webapp2.RequestHandler):
    def get(self):
        user = model.getUser(self.request.cookies.get('user',''),self.request.cookies.get('pass',''))
        if not(user):
            self.redirect('/')
            return
        if user.admin:
            self.redirect('/gensettings.html')
            return
        if user.studentgroupname:
            self.redirect('/groupcalendar.html')
            return
        tab2 = 'My Tutors'
        if user.tutor:
            tab2 = 'My Tutees'
        calendar = ''
        qry = ndb.gql("SELECT * FROM Appointments WHERE student = "+str(user.key.integer_id()))
        for appoint in qry:
            calendar+=au.getCalendarFromStudentAppointment(appoint)
        if user.tutor:
            tutorclasses = ndb.gql("SELECT * FROM TutorClasses WHERE tutor = "+str(user.key.integer_id()))
            query = ""
            for tutorclass in tutorclasses:
                if query != "":
                    query += ","
                query += str(tutorclass.key.integer_id())
            if query != "":
                qry = ndb.gql("SELECT * FROM Appointments WHERE tutorclassid in ("+query+")")
                for appoint in qry:
                    calendar+=au.getCalendarFromTutorAppointment(appoint)
        tab2url = '/'+tab2.lower().replace(' ','')+'.html'
        tab1 = 'My Calendar'
        tab1url = 'calendar.html'
        tab3 = 'My Resources'
        tab3url = 'myresources.html'
        tab4 = 'My Profile'
        tab4url = 'myprofile.html'
        template_values = {
            'logo': au.getLogo(),
            'emblem': au.getEmblem(),
            'calendar': calendar,
            'tab1': tab1,
            'tab1url': tab1url,
            'tab2': tab2,
            'tab2url': tab2url,
            'tab3': tab3,
            'tab3url': tab3url,
            'tab4': tab4,
            'tab4url': tab4url
        }
        template = JINJA_ENVIRONMENT.get_template('calendar.html')
        self.response.write(template.render(template_values))

class Landing(webapp2.RequestHandler):
    def get(self):
        template_values = {
        }
        template = JINJA_ENVIRONMENT.get_template('landing.html')
        self.response.write(template.render(template_values))

def getMajors(user):
    string = "Undecided"
    if user.major1 != "":
        query = "SELECT * FROM Departments WHERE code in ('"+user.major1+"'"
        if user.major2 != "":
            query += ",'"+user.major2+"'"
        if user.major3 != "":
            query += ",'"+user.major3+"'"
        query += ")"
        iterator = ndb.gql(query)
        for dept in iterator:
            if string == "Undecided":
                string = dept.name
            else:
                string += ",<br/>"+dept.name
    return string

def getMinors(user):
    string = "None"
    if user.minor1 != "":
        query = "SELECT * FROM Departments WHERE code in ('"+user.minor1+"'"
        if user.minor2 != "":
            query += ",'"+user.minor2+"'"
        if user.minor3 != "":
            query += ",'"+user.minor3+"'"
        query += ")"
        iterator = ndb.gql(query)
        for dept in iterator:
            if string == "None":
                string = dept.name
            else:
                string += ",<br/>"+dept.name
    return string

class tutorsearch(webapp2.RequestHandler):
    def get(self):
        user = model.getUser(self.request.cookies.get('user',''),self.request.cookies.get('pass',''))
        if not(user):
            self.redirect('/')
            return
        template_values = {
            'tutors': tutorFullSearch()
        }
        template = JINJA_ENVIRONMENT.get_template('tutorsearch.html')
        self.response.write(template.render(template_values))

def appointmentSearch(user):
    string = ''
    appointmentlist = ndb.gql("select * from Appointments where student = "+str(user.key.integer_id())+" AND studentgroupname = ''")
    requests =ndb.gql("select * from Requests where student = "+str(user.key.integer_id()))
    for appointment in appointmentlist:
        if not(appointment.paid):
            string += au.getAppointmentInfo(appointment)
    #if requests:
    #    for request in requests:
    #        string+= au.getPendingInfo(request)
    return string
def TutorappointmentSearch(user):
    date = datetime.now()
    string = ''
    tutorclasses = ndb.gql("select * from TutorClasses where tutor = "+str(user.key.integer_id()))
    query = ''
    count = 0
    for tutorclass in tutorclasses:
        if query != '':
            query += ','
        query += str(tutorclass.key.integer_id())
        count+=1
    if count == 0:
        return "No Appointments Found."
    query = 'select * from Appointments where tutorclassid in ('+query+')'
    appointmentlist = ndb.gql(query)
    for appointment in appointmentlist :
        #if not(appointment.paid):
        day1= appointment.end.date()
        day2 =date.date()
        delta = day2 - day1
        totaldays = abs(delta.days)
        if(totaldays <=7):
            string += au.tutorApprovedAppointment(appointment)
    return string

def tutorFullSearch():
    string = ''
    tutorlist = ndb.gql("select * from Users where tutor = true")
    for tutor in tutorlist:
        if(tutor.available == True):
            string += au.getTutorSearchInfo(tutor)
    return string
def getfuturetutors():
    string=''
    query= ndb.gql("SELECT * FROM Users WHERE appliedastutor = True")
    for Users in query:
      string +=  au.printfuturtutors(Users)
   # if(string == ''):
   #     string+='No tutor applications'
    return string
def getclassrequest():
    string=''
    query= ndb.gql("SELECT * FROM TutorClasses WHERE approved= False")
    for Tutorclasses in query:
      string +=  au.printrequestedclasses(Tutorclasses)
   # if(string == ''):
       # string+='No Class applications'
    return string
class managetutors(webapp2.RequestHandler):

    def get(self):
        template_values = {
            'logo': au.getLogo(),
            'emblem': au.getEmblem(),
            'tab1': 'General Settings',
            'tab1url': '/gensettings.html',
            'tab2': 'Manage Tutors',
            'tab2url': '/managetutors.html',
            'tab3': 'Student Groups',
            'tab3url': '/gensettings.html',
            'tab4': 'Manage Resources',
            'tab4url': '/adminresources.html',
            'futuretutors':getfuturetutors(),
            'classes':getclassrequest()
        }
        template = JINJA_ENVIRONMENT.get_template('managetutors.html')
        self.response.write(template.render(template_values))

class myprofile(webapp2.RequestHandler):
    def get(self):
        user = model.getUser(self.request.cookies.get('user',''),self.request.cookies.get('pass',''))
        wepayaccountinfo = ''
        addsponsor =''
        minimumstring=''
        available =''
        if not(user):
            self.redirect('/')
            return
        status = 'Student'
        avatar = 'statics/images/profilepic.png'
        if user.avatar:
            avatar = '/viewPhoto/'+user.avatar.__str__()
        searchfunction = 'searchStudentClasses()'
        tutorapply = "<button id='areyousurebutton'>REQUEST TO BE A TUTOR</button><br />"
        if user.available:
            available =getAvailabilities(user)

        if (user.appliedastutor):
            tutorapply = "<p>Your request to be a tutor has been sent.</p>"
        if (user.tutor):
            status = 'Tutor'
            minimumstring = '<p style="font-size: 0.85em; font-weight: normal; border: 1px solid #f5f5f5; background-color: #f5f5f5; padding: 10px 20px;"><span style="color: #f68e56; font-weight: bold;">NOTE:</span> "<span style="color: #0093e7;">ONLY </span>" ADD CLASSES THAT YOU ARE AN EXPERT AT TEACHING</p>'
            searchfunction = 'searchTutorClasses()'
            if (user.wepayuid =='0' or user.wepayuid ==''):
                wepayaccountinfo = au.wepayinformation(user)
            elif (user.wepayuid !='0' or user.wepayuid !=''):
                wepayaccountinfo= '<tr><td width=10% colspan="1">For more information about your wepay transactions <a href="https://wepay.com">CLICK HERE </a> </td></tr>'
            tutorapply = ''
        tab2 = 'My Tutors'
        if user.tutor:
            tab2 = 'My Tutees'
        studentgroups = ndb.gql("SELECT * FROM Users WHERE studentgroupname != ''")
        studentgroupstring = ''
        if not user.tutor:
            addsponsor='<div id='+'studentgroupselect'+'>REGISTER WITH A STUDENT GROUP</div>'
        for studentgroup in studentgroups:
            studentgroupstring += '<option value="'+studentgroup.studentgroupname+'">'+studentgroup.studentgroupname+'</option>'
        majors = getMajors(user)
        minors = getMinors(user)
        years = ['Freshman','Sophomore','Junior','Senior']
        tab2url = '/'+tab2.lower().replace(' ','')+'.html'
        tab1 = 'My Calendar'
        tab1url = 'calendar.html'
        tab3 = 'My Resources'
        tab3url = 'myresources.html'
        tab4 = 'My Profile'
        tab4url = 'myprofile.html'
        
        template_values = {
            'logo': au.getLogo(),
            'emblem': au.getEmblem(),
            'firstname': user.firstname,
            'lastname': user.lastname,
            'fullname': user.fullname,
            'status': status,
            'email': user.email,
            'year': years[min(user.year-1,3)],
            'majors': majors,
            'minors': minors,
            'classes': getClasses(user),
            'sideclasses': getClassesSmall(user),
            'availability': available,
            'minavailability': getSideAvailabilities(user),
            'departments': model.getDepartmentSelect(),
            'userid': str(user.key.integer_id()),
            #'studentgroups': studentgroupstring,
            'searchfunction': searchfunction,
            'avatar': avatar,
            'tutorapply': tutorapply,
            'tab1': tab1,
            'tab1url': tab1url,
            'tab2': tab2,
            'tab2url': tab2url,
            'tab3': tab3,
            'tab3url': tab3url,
            'tab4': tab4,
            'tab4url': tab4url,
            'wepayaccountinfo':wepayaccountinfo,
            'client_id':client_id,
            'fullname': user.fullname,
            'email': user.email,
            #'addsponsor':addsponsor,
            'minimumstring':minimumstring,
            'phonenumber':user.phone,
            'available':au.vacationbutton(user)
        }
        template = JINJA_ENVIRONMENT.get_template('myprofile.html')
        self.response.write(template.render(template_values))

class ViewPhotoHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, photo_key):
        if not blobstore.get(photo_key):
            self.error(404)
        else:
            self.send_blob(photo_key)

def getSideAvailabilities(user):
    qry = ndb.gql("SELECT * FROM Availabilities WHERE user = "+str(user.key.integer_id())+" ORDER BY dayofweek, start")
    string = ''
    avails = []
    days = ['Su','M','T','W','Th','F','Sa']
    for avail in qry:
        avails.append(avail)
    for i in range(7):
        daystring = '<tr><td valign="top">'+days[i]+':</td><td><table border="0" cellspacing="0" cellpadding="0">'
        timestring = ''
        for avail in avails:
            if avail.dayofweek == i:
                timestring+='<tr><td><span class="timepref">'
                timestring+=au.formattime(avail.start)+' - '+au.formattime(avail.end)
                timestring+='</span></td></tr>'
        if timestring != '':
            string+=daystring+timestring+'</table></td></tr>'
    return string

def getAvailabilities(user):
    qry = ndb.gql("SELECT * FROM Availabilities WHERE user = "+str(user.key.integer_id())+" ORDER BY dayofweek, start")
    string = ''
    avails = []
    days = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
    for avail in qry:
        avails.append(avail)
    for i in range(7):
        daystring = '<tr><td class="col_title">'+days[i]+':</td><td></td>'
        daystring+= '<td class="col_title">Delete?</td></tr>'

        timestring = ''
        for avail in avails:
            if avail.dayofweek == i:
                timestring+='<tr><td class="avail_time">'
                timestring+=au.formattime(avail.start)+' - '+au.formattime(avail.end)
                timestring+='</td><td></td>'
                timestring+='</select></td><td class="class_status" align="center"><img class="del-avail" onclick="setAvailToDelete('+str(avail.key.integer_id())+');" src="statics/images/minus.png" /></td></tr>'
        if timestring != '':
            string+=daystring+timestring+'<tr><td></td><td></td><td></td></tr>'
    return string

def getClassesSmall(user):
    qry = ndb.gql("SELECT * FROM StudentClasses WHERE student = "+user.key.integer_id().__str__())
    string = ''
    classnum = 1
    colors = ['black','orange','blue']
    for mystudentclass in qry:
        myclass = model.Classes.get_by_id(mystudentclass.class_id)
        string+='<span id="mini'+str(mystudentclass.key.integer_id())+'" class="status_'+colors[mystudentclass.status]+'"></span>'+myclass.department+' '+myclass.coursenumber.__str__()+'<br />'
    return string

def getClasses(user):
    if user.tutor:
        return getTutorClasses(user)
    qry = ndb.gql("SELECT * FROM StudentClasses WHERE student = "+user.key.integer_id().__str__())
    string = ''
    classnum = 1
    for mystudentclass in qry:
        myclass = model.Classes.get_by_id(mystudentclass.class_id)
        if myclass:
            string += au.getClassHTML(myclass,classnum,mystudentclass.status,mystudentclass.key.integer_id())
            classnum += 1
    return string +'</tr>'

def getTutorClasses(user):
    qry = ndb.gql("SELECT * FROM TutorClasses WHERE tutor = "+user.key.integer_id().__str__())
    string = ''
    classnum = 1
    for mytutorclass in qry:
        myclass = model.Classes.get_by_id(mytutorclass.class_id)
        if mytutorclass.approved:
            if myclass:
                string += au.getTutorClassHTML(myclass,classnum,mytutorclass.rate,mytutorclass.key.integer_id())
                classnum += 1
    return string +'</tr>'
    #write a function for just the tutors email!

class mytutors(webapp2.RequestHandler):
    def get(self):
        user = model.getUser(self.request.cookies.get('user',''),self.request.cookies.get('pass',''))
        if not(user):
            self.redirect('/')
            return
        tab2 = 'My Tutors'
        if user.tutor:
            tab2 = 'My Tutees'
        status = 'Student'
        if (user.tutor):
            status = 'Tutor'
        avatar = 'statics/images/profilepic.png'
        if user.avatar:
            avatar = '/viewPhoto/'+user.avatar.__str__()
        studentgroupstring = ''
        studentgroups = ndb.gql("SELECT * FROM StudentGroups WHERE student = "+str(user.key.integer_id()))
        for studentgroup in studentgroups:
            studentgroupstring += '<option>'+studentgroup.groupname+'</option>'
        years = ['Freshman','Sophomore','Junior','Senior']
        tab2url = '/'+tab2.lower().replace(' ','')+'.html'
        tab1 = 'My Calendar'
        tab1url = 'calendar.html'
        tab3 = 'My Resources'
        tab3url = 'myresources.html'
        tab4 = 'My Profile'
        tab4url = 'myprofile.html'
        template_values = {
            'logo': au.getLogo(),
            'emblem': au.getEmblem(),
            'firstname': user.firstname,
            'lastname': user.lastname,
            'fullname': user.fullname,
            'status': status,
            'majors': getMajors(user),
            'minors': getMinors(user),
            'year': years[min(user.year-1,3)],
            'avatar': avatar,
            'tutors': appointmentSearch(user)+tutorFullSearch(),
            'studentgroups': studentgroupstring,
            'tab1': tab1,
            'tab1url': tab1url,
            'tab2': tab2,
            'tab2url': tab2url,
            'tab3': tab3,
            'tab3url': tab3url,
            'tab4': tab4,
            'tab4url': tab4url
        }
        template = JINJA_ENVIRONMENT.get_template('mytutors.html')
        self.response.write(template.render(template_values))
    def post(self):
        user = model.getUser(self.request.cookies.get('user',''),self.request.cookies.get('pass',''))
        status = 'Student'
        if (user.tutor):
            status = 'Tutor'
        tab2 = 'My Tutors'
        if user.tutor:
            tab2 = 'My Tutees'
        avatar = 'statics/images/profilepic.png'
        if user.avatar:
            avatar = '/viewPhoto/'+user.avatar.__str__()
        studentgroupstring = ''
        studentgroups = ndb.gql("SELECT * FROM StudentGroups WHERE student = "+str(user.key.integer_id()))
        for studentgroup in studentgroups:
            studentgroupstring += '<option>'+studentgroup.groupname+'</option>'
        years = ['Freshman','Sophomore','Junior','Senior']
        tab2url = '/'+tab2.lower().replace(' ','')+'.html'
        tab1 = 'My Calendar'
        tab1url = 'calendar.html'
        tab3 = 'My Resources'
        tab3url = 'myresources.html'
        tab4 = 'My Profile'
        tab4url = 'myprofile.html'
        template_values = {
            'logo': au.getLogo(),
            'emblem': au.getEmblem(),
            'firstname': user.firstname,
            'lastname': user.lastname,
            'fullname': user.fullname,
            'status': status,
            'majors': getMajors(user),
            'minors': getMinors(user),
            'year': years[min(user.year-1,3)],
            'avatar': avatar,
            'studentgroups': studentgroupstring,
            'tutors': tutorQuery(self.request.get("mysearch")),
            'tab1': tab1,
            'tab1url': tab1url,
            'tab2': tab2,
            'tab2url': tab2url,
            'tab3': tab3,
            'tab3url': tab3url,
            'tab4': tab4,
            'tab4url': tab4url
        }
        template = JINJA_ENVIRONMENT.get_template('mytutors.html')
        self.response.write(template.render(template_values))

class mytutees(webapp2.RequestHandler):
    def get(self):
        user = model.getUser(self.request.cookies.get('user',''),self.request.cookies.get('pass',''))
        if not(user):
            self.redirect('/')
            return
        if not(user.tutor):
            self.redirect('/mytutors.html')
            return
        tab2 = 'My Tutees'
        status = 'Tutor'
        avatar = 'statics/images/profilepic.png'
        if user.avatar:
            avatar = '/viewPhoto/'+user.avatar.__str__()
        years = ['Freshman','Sophomore','Junior','Senior']
        tab2url = '/'+tab2.lower().replace(' ','')+'.html'
        tab1 = 'My Calendar'
        tab1url = 'calendar.html'
        tab3 = 'My Resources'
        tab3url = 'myresources.html'
        tab4 = 'My Profile'
        tab4url = 'myprofile.html'
        template_values = {
            'logo': au.getLogo(),
            'emblem': au.getEmblem(),
            'firstname': user.firstname,
            'lastname': user.lastname,
            'fullname': user.fullname,
            'status': status,
            'majors': getMajors(user),
            'minors': getMinors(user),
            'year': years[min(user.year-1,3)],
            'tutors': tuteeFullSearch(user),
            'approved':TutorappointmentSearch(user),
            'avatar': avatar,
            'tab1': tab1,
            'tab1url': tab1url,
            'tab2': tab2,
            'tab2url': tab2url,
            'tab3': tab3,
            'tab3url': tab3url,
            'tab4': tab4,
            'tab4url': tab4url
        }
        template = JINJA_ENVIRONMENT.get_template('mytutees.html')
        self.response.write(template.render(template_values))
    def post(self):
        user = model.getUser(self.request.cookies.get('user',''),self.request.cookies.get('pass',''))
        if not(user.tutor):
            self.redirect('/mytutors.html')
        status = 'Tutor'
        tab2 = 'My Tutees'
        years = ['Freshman','Sophomore','Junior','Senior']
        tab2url = '/'+tab2.lower().replace(' ','')+'.html'        
        tab1 = 'My Calendar'
        tab1url = 'calendar.html'
        tab3 = 'My Resources'
        tab3url = 'myresources.html'
        tab4 = 'My Profile'
        tab4url = 'myprofile.html'
        template_values = {
            'logo': au.getLogo(),
            'emblem': au.getEmblem(),
            'firstname': user.firstname,
            'lastname': user.lastname,
            'fullname': user.fullname,
            'status': status,
            'majors': getMajors(user),
            'minors': getMinors(user),
            'year': years[min(user.year-1,3)],
            'tutors': tutorQuery(self.request.get("mysearch")),
            'tab1': tab1,
            'tab1url': tab1url,
            'tab2': tab2,
            'tab2url': tab2url,
            'tab3': tab3,
            'tab3url': tab3url,
            'tab4': tab4,
            'tab4url': tab4url
        }
        template = JINJA_ENVIRONMENT.get_template('mytutees.html')
        self.response.write(template.render(template_values))

def tuteeFullSearch(user):
    string = ''
    tutorclasses = ndb.gql("select * from TutorClasses where tutor = "+str(user.key.integer_id()))
    query = ''
    count = 0
    for tutorclass in tutorclasses:
        if query != '':
            query += ','
        query += str(tutorclass.key.integer_id())
        count+=1
    if count == 0:
        return "No Requests Found."
    query = 'select * from Requests where tutorclassid in ('+query+')'
    requests = ndb.gql(query)
    for request in requests:
        string += au.getRequestInfo(request)
    return string

def tutorQuery(search):
    string = ''
    tutors = []
    tutorlist = ndb.gql("select * from Users where firstname = '"+search+"'")
    for tutor in tutorlist:
        tutors.append(tutor.key.integer_id())
    tutorlist = ndb.gql("select * from Users where lastname = '"+search+"'")
    for tutor in tutorlist:
        tutors.append(tutor.key.integer_id())
    tutorlist = ndb.gql("select * from Users where fullname = '"+search+"'")
    for tutor in tutorlist:
        tutors.append(tutor.key.integer_id())
    obj = getClassCode(search)
    if obj:
        myclass = ndb.gql("select * from Classes where coursenumber = "+obj[1].__str__()+" and department = '"+obj[0].upper()+"'").get()
        if myclass:
            tutorclasslist = ndb.gql("select * from TutorClasses where class_id = "+str(myclass.key.integer_id()))
            for tutorclass in tutorclasslist:
                tutors.append(tutorclass.tutor)
    for tutorid in tutors:
        #tutors.append(tutor.key.integer_id())
        tutor = model.Users.get_by_id(tutorid)
        string += au.getTutorSearchInfo(tutor)
    return string

def getClassCode(string):
    try:
        num = 0
        if len(string) == 7:
            num = int(string[4:])
        elif string[4] != ' ':
            return false
        else:
            num = int(string[5:])
        if num >= 100 and num < 1000:
            return [string[:4],num]
    except:
        return False

class myresources(webapp2.RequestHandler):
    def get(self):
        user = model.getUser(self.request.cookies.get('user',''),self.request.cookies.get('pass',''))
        status = 'Student'
        if (user.tutor):
            status = 'Tutor'
        tab2 = 'My Tutors'
        if user.tutor:
            tab2 = 'My Tutees'
        avatar = 'statics/images/profilepic.png'
        if user.avatar:
            avatar = '/viewPhoto/'+user.avatar.__str__()
        years = ['Freshman','Sophomore','Junior','Senior']
        tab2url = '/'+tab2.lower().replace(' ','')+'.html'
        tab1 = 'My Calendar'
        tab1url = 'calendar.html'
        tab3 = 'My Resources'
        tab3url = 'myresources.html'
        tab4 = 'My Profile'
        tab4url = 'myprofile.html'
        resources = ''
        resourcelist = ndb.gql("SELECT * FROM Resources ORDER BY order")
        for resource in resourcelist:
            resources += resource.html
        template_values = {
            'logo': au.getLogo(),
            'emblem': au.getEmblem(),
            'firstname': user.firstname,
            'lastname': user.lastname,
            'fullname': user.fullname,
            'status': status,
            'majors': getMajors(user),
            'minors': getMinors(user),
            'year': years[min(user.year-1,3)],
            'avatar': avatar,
            'tab1': tab1,
            'tab1url': tab1url,
            'tab2': tab2,
            'tab2url': tab2url,
            'tab3': tab3,
            'tab3url': tab3url,
            'tab4': tab4,
            'tab4url': tab4url,
            'resources': resources
        }
        template = JINJA_ENVIRONMENT.get_template('myresources.html')
        self.response.write(template.render(template_values))

class Register(webapp2.RequestHandler):
    def get(self):
        template_values = {
        }
        template = JINJA_ENVIRONMENT.get_template('reg1.html')
        self.response.write(template.render(template_values))
class RegisterReplace(webapp2.RequestHandler):
    def get(self):
        user = model.getUser(self.request.cookies.get('user',''),self.request.cookies.get('pass',''))
        avatar = 'statics/images/profilepic.png'
        if user.tos == True:
            self.redirect('/calendar.html')
        if user.avatar:
            avatar = '/viewPhoto/'+user.avatar.__str__()
        template_values = {
            'name':user.fullname,
            'email':user.email,
            'password':hashlib.sha224(user.password).hexdigest(),
            'year':user.year,
            'major':user.major1,
            'avatar':avatar,
            'minor':user.minor1}
        
        template = JINJA_ENVIRONMENT.get_template('reg.html')
        self.response.write(template.render(template_values))

class TOS(webapp2.RequestHandler):
    def get(self):
        template_values = {
        }
        template = JINJA_ENVIRONMENT.get_template('tos.html')
        self.response.write(template.render(template_values))


class LogIn(webapp2.RequestHandler):

    def post(self):
        redirecte ='/calendar.html'
        username = self.request.get('username')
        user = model.getUserNoPassword(username)
        if not(user):
            self.redirect('/')
            return
        password = hashlib.sha224(self.request.get('password')).hexdigest()
        if not(password==user.password):
            self.redirect('/')
            return
        if not(user.admin):
            if (user.tos == False):
                redirecte ='/reg.html'
        self.response.headers.add_header( "Set-Cookie","user=%s; path=/" % username.__str__())
        self.response.headers.add_header( "Set-Cookie","pass=%s; path=/" % self.request.get('password').__str__())
        self.redirect(redirecte)

class LogOut(webapp2.RequestHandler):
    def get(self):
        self.response.headers.add_header( "Set-Cookie","user=%s; path=/" % '')
        self.response.headers.add_header( "Set-Cookie","pass=%s; path=/" % '')
        self.redirect('/')

class ModifyUser(webapp2.RequestHandler):
    def post(self):
        user = model.getUser(self.request.cookies.get('user',''),self.request.cookies.get('pass',''))
        checkbox = self.request.get('tos')
        if(checkbox == 'on'):
            user.tos = True;
        #CODE TO MODIFY USER
        #self.request.get('tos')
        user.put()
        self.redirect('/calendar.html')
        
class CreateUser(webapp2.RequestHandler):
    def post(self):
        tosvar = False;
        if(self.request.get('tos')== 'on'):
                tosvar = True;
        user = model.Users(username = self.request.get('username'),
                     password = hashlib.sha224(self.request.get('password')).hexdigest(),
                     firstname = self.request.get('firstname'),
                     lastname = self.request.get('lastname'),
                     fullname = self.request.get('firstname')+' '+self.request.get('lastname'),
                     phone = self.request.get('phonenumber'),
                     email = self.request.get('email'),
                     aboutme = self.request.get('aboutme'),
                   #  major1 = self.request.get('major1'),
                   #  major2 = self.request.get('major2'),
                   #  major3 = self.request.get('major3'),
                   #  minor1 = self.request.get('minor1'),
                   #  minor2 = self.request.get('minor2'),
                   #  minor3 = self.request.get('minor3'),
                     wepayuid= self.request.get('wepayuid'),
                     wepayat = self.request.get('wepayat'),
                     tutor = False,
                     avatar = None,
                     year = 4,
                     appliedastutor = False,
                     tos = tosvar,
                     admin = False,
                     available = True,
                     studentgroupname = '')
        user.put()

        username = self.request.get('username')
        password = hashlib.sha224(self.request.get('password')).hexdigest()
        
        self.response.headers.add_header( "Set-Cookie","user=%s; path=/" % username.__str__())
        self.response.headers.add_header( "Set-Cookie","pass=%s; path=/" % self.request.get('password').__str__())
        
        self.response.write('User Created!')
        avatarfile = ''
        avatarfile = self.request.get('avatarfile','')
        if(avatarfile != ''):
            form_fields = {
                "file": self.request.get('avatarfile2')
                }
            form_data = urllib.urlencode(form_fields)
            result = urlfetch.fetch(url=avatarfile,
                                    payload=form_data,
                                    method=urlfetch.POST,
                                    headers={'Content-Type': 'application/x-www-form-urlencoded'})

        self.redirect('/')


class StudentGroupPay(webapp2.RequestHandler):
    def post(self):
        user = model.getUser(self.request.cookies.get('user',''),self.request.cookies.get('pass',''))
        if not(user):
            self.redirect('/')
            return
        appointment = model.Appointments.get_by_id(int(self.request.get('apptid')))
        if user.key.integer_id() != appointment.student:
            self.redirect('/')
            return
        appointment.studentgroupname = self.request.get('studentgroup')
        appointment.put()
        time.sleep(.5)
        self.redirect('/mytutors.html')

class SendRequest(webapp2.RequestHandler):
    def post(self):
        user = model.getUser(self.request.cookies.get('user',''),self.request.cookies.get('pass',''))
        if not(user):
            self.redirect('/')
            return
        tci = int(self.request.get('tutorclassid'))
        tutorclass = model.TutorClasses.get_by_id(tci)
        request = model.Requests(
            tutorclassid = tci,
            student = user.key.integer_id(),
            notes = self.request.get('notes'))
        request.put()
        rid = request.key.integer_id()
        line = 1
        linestr = str(line)
        while self.request.get('start'+linestr,"") != '' and self.request.get('date'+linestr,""):
            date = self.request.get('date'+linestr).split('-')
            year = int(date[0])
            month = int(date[1])
            day = int(date[2])
            start = int(self.request.get('start'+linestr))
            end = int(self.request.get('end'+linestr))
            totalcost = (end - start) * tutorclass.rate
            starttime = datetime(year,month,day,start)
            endtime = datetime(year,month,day,end)
            requestLine = model.RequestLines(
                requestid = rid,
                start = starttime,
                end = endtime,
                cost = totalcost)
            requestLine.put()
            line = line + 1
            linestr = str(line)
        self.redirect('/mytutors.html')

class AddAdminData(webapp2.RequestHandler):
    def get(self):
        settings = model.Settings(
            logo = None,
            emblem = None,
            allowratings = True,
            tutorsetrate = False,
            tutorrate = 0)
        settings.put()

class AddTestData(webapp2.RequestHandler):
    def get(self):

        #studentclass = model.StudentClasses(
        #    class_id = 5838406743490560,
        #    student = 5733953138851840,
        #    status = 0
        #    )
        #studentclass.put()
        #availability = model.Availabilities(
        #    user = 5681726336532480,
        #    dayofweek = 0,
        #    start = datetime.now().time(),
        #    end = datetime.now().time())
        #availability.put()
        # x = 0
        # tutorlist = ndb.gql("select * from Users")
        # for Users in tutorlist:
        #     Users.key.delete()
        # while x < 500:
        #     tutor = model.Users(
        #         username = "email" + str(x) + "@email.com",
        #         password = "d63dc919e201d7bc4c825630d2cf25fdc93d4b2f0d46706d29038d01",
        #         firstname = "tutor1",
        #         lastname = "wann",
        #         fullname = "tutor1 Wann",
        #         phone = "302545893",
        #         email =  "email" + str(x) + "@email.com",
        #         tutor = True,
        #         aboutme = "I love Cartoons",
        #         major1 = "MATH",
        #         minor1 = "MATH",
        #         year = 4
        #     )
        #     tutor.put()
        #     x+=1
        # y = 0
        # while y < 500:
        #     student = model.Users(
        #         username = "email" + str(x) + "@email.com",
        #         password = "d63dc919e201d7bc4c825630d2cf25fdc93d4b2f0d46706d29038d01",
        #         firstname = "Hey",
        #         lastname = "Arnold",
        #         fullname = "Hey Arnold",
        #         phone = "302545893",
        #         email =  "email" + str(x) + "@email.com",
        #         tutor = False,
        #         aboutme = "I love Cartoons",
        #         major1 = "MATH",
        #         minor1 = "MATH",
        #         year = 4
        #     )
        #     student.put()
        #     y+=1
        myclass = model.Classes(
            department = "MATH",
            coursenumber = 001,
            classname = "Discrete Mathematics",
            active = True,
            semester = 1,
            year = 2015
            )
        myclass.put()
        myclass1 = model.Classes(
            department = "MATH",
            coursenumber = 002,
            classname = "Calculus 1",
            active = True,
            semester = 1,
            year = 2015
            )
        myclass1.put()
        myclass2 = model.Classes(
            department = "MATH",
            coursenumber = 003,
            classname = "Calculus 2",
            active = True,
            semester = 1,
            year = 2015
            )
        myclass2.put()
        myclass3 = model.Classes(
            department = "MATH",
            coursenumber = 004,
            classname = "Calculus 3",
            active = True,
            semester = 1,
            year = 2015
            )
        myclass3.put()
        myclass800 = model.Classes(
            department = "MATH",
            coursenumber = 005,
            classname = "Algebra 1",
            active = True,
            semester = 1,
            year = 2015
            )
        myclass800.put()
        myclass900 = model.Classes(
            department = "MATH",
            coursenumber = 006,
            classname = "Algebra 2",
            active = True,
            semester = 1,
            year = 2015
            )
        myclass900.put()
        myclass900 = model.Classes(
            department = "MATH",
            coursenumber = 007,
            classname = "Elementary Math",
            active = True,
            semester = 1,
            year = 2015
            )
        myclass900.put()  
        myclass5 = model.Classes(
            department = "HIST",
            coursenumber = 001,
            classname = "US History 1",
            active = True,
            semester = 1,
            year = 2015
            )
        myclass5.put()
        myclass6 = model.Classes(
            department = "HIST",
            coursenumber = 002,
            classname = "US History 2",
            active = True,
            semester = 1,
            year = 2015
            )
        myclass6.put()
        myclass100 = model.Classes(
            department = "HIST",
            coursenumber = 003,
            classname = "World History ",
            active = True,
            semester = 1,
            year = 2015
            )
        myclass100.put()
        myclass200 = model.Classes(
            department = "HIST",
            coursenumber = 004,
            classname = "AP US History ",
            active = True,
            semester = 1,
            year = 2015
            )
        myclass200.put()
        myclass300 = model.Classes(
            department = "HIST",
            coursenumber = 005,
            classname = "AP Government",
            active = True,
            semester = 1,
            year = 2015
            )
        myclass300.put()
        myclass500 = model.Classes(
            department = "ENGL",
            coursenumber = 001,
            classname = "High School English ",
            active = True,
            semester = 1,
            year = 2015
            )
        myclass500.put()
        myclass600 = model.Classes(
            department = "ENGL",
            coursenumber = 002,
            classname = "Middle School English ",
            active = True,
            semester = 1,
            year = 2015
            )
        myclass600.put()
        myclass700 = model.Classes(
            department = "ENGL",
            coursenumber = 003,
            classname = "Elementary School English ",
            active = True,
            semester = 1,
            year = 2015
            )
        myclass1200 = model.Classes(
            department = "ENGL",
            coursenumber = 004,
            classname = "AP English ",
            active = True,
            semester = 1,
            year = 2015
            )
        myclass1200.put()
        myclass7 = model.Classes(
            department = "CHEM",
            coursenumber = 001,
            classname = "General Chemistry",
            active = True,
            semester = 1,
            year = 2015
            )
        myclass7.put()
        myclass101 = model.Classes(
            department = "CHEM",
            coursenumber = 002,
            classname = "College Chemistry",
            active = True,
            semester = 1,
            year = 2015
            )
        myclass101.put()
        myclass102 = model.Classes(
            department = "CHEM",
            coursenumber = 003,
            classname = "College Chemistry 2",
            active = True,
            semester = 1,
            year = 2015
            )
        myclass102.put()
        myclass103 = model.Classes(
            department = "PHYS",
            coursenumber = 001,
            classname = "General Physics",
            active = True,
            semester = 1,
            year = 2015
            )
        myclass103.put()
        myclass104 = model.Classes(
            department = "PHYS",
            coursenumber = 002,
            classname = "AP Physics",
            active = True,
            semester = 1,
            year = 2015
            )
        myclass104.put()
        myclass105 = model.Classes(
            department = "PHYS",
            coursenumber = 003,
            classname = "College Physics 1",
            active = True,
            semester = 1,
            year = 2015
            )
        myclass105.put()
        myclass107 = model.Classes(
            department = "PHYS",
            coursenumber = 004,
            classname = "College Physics 2",
            active = True,
            semester = 1,
            year = 2015
            )
        myclass107.put()
        mydepartement = model.Departments(
            code ='MATH',
            name= 'Mathematics'
            )
        mydepartement.put()
        mydepartement1 = model.Departments(
            code ='HIST',
            name= 'History'
            )
        mydepartement1.put()
        mydepartement2 = model.Departments(
            code ='CHEM',
            name= 'chemistry'
            )
        mydepartement2.put()
        mydepartement3 = model.Departments(
            code ='PHYS',
            name= 'Physics'
            )
        mydepartement3.put()
        mydepartement4 = model.Departments(
            code ='ENGL',
            name= 'English'
            )
        mydepartement4.put()



class AcceptRequest(webapp2.RequestHandler):
    def post(self):
        requestid = int(self.request.get('requestid'))
        request = model.Requests.get_by_id(requestid)
        lines = ndb.gql("select * from RequestLines where requestid = "+str(requestid))
        for line in lines:
            appointment = model.Appointments(
                tutorclassid = request.tutorclassid,
                student = request.student,
                start = line.start,
                end = line.end,
                cost = line.cost,
                paid = False,
                studentgroupname = '')
            appointment.put()
            student = model.Users.get_by_id(appointment.student)
            tutorclasses = model.TutorClasses.get_by_id(appointment.tutorclassid)
            tutor = model.Users.get_by_id(tutorclasses.tutor)
            line.key.delete()

            au.sendmessage(tutor.email,'Appointment Accepted','The appointment has been accepted')
            au.sendmessage(student.email, 'Appointment Accepted', 'The appointment has been accepted')
        request.key.delete()
        self.redirect('/mycalendar.html')


class ChangeSetRate(webapp2.RequestHandler):
    def get(self):
        checkbox = self.request.get('checkbox')
        settings = ndb.gql("select * from Settings")
        for item in settings:
            settings = item
        if (checkbox == 'true'):
            settings.tutorsetrate = True
        else:
            settings.tutorsetrate = False
        settings.put()
class SubmitRate(webapp2.RequestHandler):
    def get(self):
        price = float(self.request.get('price'))
        settings = ndb.gql("select * from Settings")
        for item in settings:
            settings = item

        settings.tutorrate = price
        settings.put()
        self.redirect("/gensettings.html")

class AcceptClass(webapp2.RequestHandler):
    def post(self):
        requestid = int(self.request.get('requestid'))

       # request = model.Requesttotutor.requestid(requestid)
        query = ndb.gql("select * from TutorClasses")
        for TutorClasses in query:
            if(requestid == TutorClasses.tutor):
                mytutorclasses= model.TutorClasses(
                    class_id =TutorClasses.class_id,
                    tutor = TutorClasses.tutor,
                    rate = TutorClasses.rate,
                    approved = True
                )

                mytutorclasses.put()
                TutorClasses.key.delete()
       # request.key.delete()
                tutor = model.Users.get_by_id(mytutorclasses.tutor)
                au.sendmessage(tutor.email,'Class Approved','The subject you have requested has been approved')
        self.redirect('/managetutors.html')
class DenyClass(webapp2.RequestHandler):
    def post(self):
        requestid = int(self.request.get('requestid'))
       # request = model.Requesttotutor.requestid(requestid)
        query = ndb.gql("select * from TutorClasses")
        for TutorClasses in query:
            if(requestid == TutorClasses.tutor):
                TutorClasses.key.delete()
            else:
                self.redirect('/gensettings.html')

       # request.key.delete()
            tutor = model.Users.get_by_id(TutorClasses.tutor)
            au.sendmessage(tutor.email,'Class Denied','The subject you have requested has been denied')
        self.redirect('/managetutors.html')
##################################################################################
class AcceptTutor(webapp2.RequestHandler):
    def post(self):
        requestid = int(self.request.get('requestid'))
       # request = model.Requesttotutor.requestid(requestid)
        query = ndb.gql("select * from Users")
        for Users in query:
            if(requestid == Users.key.integer_id()):
                myuser = model.Users(
                     username = Users.username,
                     password =Users.password,
                     firstname = Users.firstname,
                     lastname =Users.lastname,
                     fullname =Users.fullname,
                     phone = Users.phone,
                     email = Users.email,
                     aboutme =Users.aboutme,
                     major1 =Users.major1,
                     minor1 = Users.minor1,
                     wepayuid=Users.wepayuid,
                     wepayat =Users.wepayat,
                     tutor = True,
                     avatar = Users.avatar,
                     year = Users.year,
                     appliedastutor = False,
                     admin = False,
                     available = True,
                     studentgroupname = '',
                     tos = True)
                myuser.put()
                Users.key.delete()
       # request.key.delete()
        user = model.Users.get_by_id(myuser.email)
        au.sendmessage(myuser.email,'Tutor Approved','You have been approved  a tutor')
        self.redirect('/managetutors.html')
class Denytutor(webapp2.RequestHandler):
    def post(self):
        requestid = int(self.request.get('requestid'))
       # request = model.Requesttotutor.requestid(requestid)
        query = ndb.gql("select * from Users")
        for Users in query:
            if(requestid == Users.key.integer_id()):
                myuser = model.Users(
                     username = Users.username,
                     password =Users.password,
                     firstname = Users.firstname,
                     lastname =Users.lastname,
                     fullname =Users.fullname,
                     phone = Users.phone,
                     email = Users.email,
                     aboutme =Users.aboutme,
                     major1 =Users.major1,
                     minor1 = Users.minor1,
                     wepayuid=Users.wepayuid,
                     wepayat =Users.wepayat,
                     tutor = False,
                     avatar = Users.avatar,
                     year = Users.year,
                     appliedastutor = False,
                     admin = False,
                     available = True,
                     studentgroupname = '')
                myuser.put()
                Users.key.delete()
       # request.key.delete()
        user = model.Users.get_by_id(myuser.email)
        au.sendmessage(myuser.email, 'Tutor Rejected', 'You have not been approved to become a tutor')
        self.redirect('/managetutors.html')
class GoonVacation(webapp2.RequestHandler):
    def get(self):
        curUser = model.getUser(self.request.cookies.get('user',''),self.request.cookies.get('pass',''))
        curUser.available = False
        curUser.put()
        time.sleep(1)
        self.redirect('/myprofile.html')
class comebackfromvacation(webapp2.RequestHandler):
    def get(self):
        curUser = model.getUser(self.request.cookies.get('user',''),self.request.cookies.get('pass',''))
        curUser.available = True
        curUser.put()
        time.sleep(1)
        self.redirect('/myprofile.html')
class ApplyAsTutor(webapp2.RequestHandler):
    def get(self):
        curUser = model.getUser(self.request.cookies.get('user',''),self.request.cookies.get('pass',''))
        curUser.appliedastutor = True
        curUser.put()
        time.sleep(1)
        self.redirect('/myprofile.html')
#Put delete appointment

class AddAvailability(webapp2.RequestHandler):
    def post(self):
        curUser = model.getUser(self.request.cookies.get('user',''),self.request.cookies.get('pass',''))
        starthour = int(self.request.get('starttime'))
        endhour = int(self.request.get('endtime'))
        addAvailability(curUser.key.integer_id(),int(self.request.get('dayofweek')),starthour,endhour)
        time.sleep(.5)
        self.redirect('/myprofile.html')

class CancelAppointment(webapp2.RequestHandler):
    def post(self):
        user = model.getUser(self.request.cookies.get('user',''),self.request.cookies.get('pass',''))
        apptid = int(self.request.get('cancelapptid'))
        #TODO add validation
        appt = model.Appointments.get_by_id(apptid)
        student = model.Users.get_by_id(appt.student)
        tutorclass = model.TutorClasses.get_by_id(appt.tutorclassid)
        tutor = model.Users.get_by_id(tutorclass.tutor)
        if appt.paid and appt.checkoutid != 0:
            resp = au.refund(appt.checkoutid, tutor.wepayat)
        if(str(resp) == "Error"):
            self.redirect('error.html')
        else:
            au.sendmessage(student,'Appointment has been cancelled','Appointment has been cancelled.')
            au.sendmessage(tutor,'Appointment has been cancelled','Appointment has been cancelled.')
            appt.key.delete()
            time.sleep(.5)
            self.redirect('/mytutees.html')

class Error(webapp2.RequestHandler):
    def get(self):
        template_values = {
            'error':'It seems the payment has yet to be completely authorized. </ br>Please wait a moment and try again.'
        }
        template = JINJA_ENVIRONMENT.get_template('error.html')
        self.response.write(template.render(template_values))

class Error2(webapp2.RequestHandler):
    def get(self):
        template_values = {
            'error':'This tutor does not have a wepay account.</ br>Please contact them of this or pay them in person.'
        }
        template = JINJA_ENVIRONMENT.get_template('error.html')
        self.response.write(template.render(template_values))

class RequestStudentGroup(webapp2.RequestHandler):
    def post(self):
        curUser = model.getUser(self.request.cookies.get('user',''),self.request.cookies.get('pass',''))
        request = model.StudentGroupRequests(
            student = curUser.key.integer_id(),
            groupname = self.request.get('studentgroup'))
        request.put()
        self.redirect('/myprofile.html')

def addAvailability(userkey, dayofweek, starthour, endhour):
    overlapped = ndb.gql("select * from Availabilities "+
                         "where user = "+str(userkey)+" "+
                         "and dayofweek = "+str(dayofweek)+" "
                         "and start >= TIME("+str(starthour)+",0,0) "+
                         "and start <= TIME("+str(endhour)+",0,0)")
    for avail in overlapped:
        avail.key.delete()
        addAvailability(userkey,dayofweek,starthour,max(endhour,avail.end.hour))
        return
    overlapped = ndb.gql("select * from Availabilities "+
                         "where user = "+str(userkey)+" "+
                         "and dayofweek = "+str(dayofweek)+" "
                         "and end >= TIME("+str(starthour)+",0,0) "+
                         "and end <= TIME("+str(endhour)+",0,0)")
    for avail in overlapped:
        avail.key.delete()
        addAvailability(userkey,dayofweek,max(endhour,avail.end.hour),endhour)
        return
    avail = model.Availabilities(
            user = userkey,
            dayofweek = dayofweek,
            start = datetime(1970,1,1,starthour,0,0).time(),
            end = datetime(1970,1,1,endhour,0,0).time()
            )
    avail.put()

class UploadPhoto(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        user = model.getUser(self.request.cookies.get('user',''),self.request.cookies.get('pass',''))
        redirect = '/myprofile.html'
        redirect = self.request.get('redirect','/myprofile.html')
        if not(user):
            self.redirect('/')
            return
        old_key = user.avatar
        if old_key:
            blobstore.delete(old_key)
        upload_files = self.get_uploads('file')  # 'file' is file upload field in the form
        upload = upload_files[0]
        user.avatar = upload.key()
        user.put()
        time.sleep(1)
        self.redirect(redirect)

class UploadLogo(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        user = model.getUser(self.request.cookies.get('user',''),self.request.cookies.get('pass',''))
        if not(user):
            self.redirect('/')
            return
        if not(user.admin):
            self.redirect('/')
            return
        settings = None
        query = ndb.gql("select * from Settings")
        for item in query:
            settings = item
        old_key = settings.logo
        if old_key:
            blobstore.delete(old_key)
        upload_files = self.get_uploads('file')  # 'file' is file upload field in the form
        upload = upload_files[0]
        settings.logo = upload.key()
        settings.put()
        time.sleep(1)
        self.redirect('/gensettings.html')
        
class UploadEmblem(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        user = model.getUser(self.request.cookies.get('user',''),self.request.cookies.get('pass',''))
        if not(user):
            self.redirect('/')
            return
        if not(user.admin):
            self.redirect('/')
            return
        settings = None
        query = ndb.gql("select * from Settings")
        for item in query:
            settings = item
        old_key = settings.emblem
        if old_key:
            blobstore.delete(old_key)
        upload_files = self.get_uploads('file')  # 'file' is file upload field in the form
        upload = upload_files[0]
        settings.emblem = upload.key()
        settings.put()
        time.sleep(1)
        self.redirect('/gensettings.html')

class UploadResource(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        user = model.getUser(self.request.cookies.get('user',''),self.request.cookies.get('pass',''))
        if not(user):
            self.redirect('/')
            return
        if not(user.admin):
            self.redirect('/')
            return
        upload_files = self.get_uploads('file')  # 'file' is file upload field in the form
        upload = upload_files[0]
        max_order = 0
        query = ndb.gql("select * from Resources")
        for res in query:
            if res.order > max_order:
                max_order = res.order
        resource = model.Resources(
            html = '<br/> <br/> <img style="margin-right:20px"src="/viewPhoto/'+str(upload.key())+'" /> </i>',
            order = max_order+1)
        resource.put()
        time.sleep(1)
        self.redirect('/adminresources.html')

class UploadStringResource(webapp2.RequestHandler):
    def post(self):
        user = model.getUser(self.request.cookies.get('user',''),self.request.cookies.get('pass',''))
        if not(user):
            self.redirect('/')
            return
        if not(user.admin):
            self.redirect('/')
            return
        max_order = 0
        query = ndb.gql("select * from Resources")
        for res in query:
            if res.order > max_order:
                max_order = res.order
        resource = model.Resources(
            html = self.request.get('html'),
            order = max_order+1)
        resource.put()
        time.sleep(1)
        self.redirect('/adminresources.html')

class Database(webapp2.RequestHandler):
    def __init__(self, *args, **kwargs):
        webapp2.RequestHandler.__init__(self, *args, **kwargs)
        self.methods = RPCMethods()
    def get(self):
        func = None
        action = self.request.get('action')
        redirect = ''
        redirect = self.request.get('redirect','')
        if action:
            if action[0]=='_':
                self.error(403)
                return
            else:
                func = getattr(self.methods,action, None)
        if not(func):
            self.error(403)
            return
        args = ()
        while True:
            key = 'arg%d' % len(args)
            val = self.request.get(key)
            if val:
                args += (val,)
            else:
                break
        result = func(*args)
        self.response.out.write(result)

class RPCMethods():
    def photoURL(self, *args):
        return blobstore.create_upload_url('/uploadPhoto')
    def logoURL(self, *args):
        return blobstore.create_upload_url('/uploadLogo')
    def emblemURL(self, *args):
        return blobstore.create_upload_url('/uploadEmblem')
    def resourceURL(self, *args):
        return blobstore.create_upload_url('/uploadResource')
    def updateClassStatus(self, *args):
        mystudentclass = model.StudentClasses.get_by_id(int(args[0]))
        mystudentclass.status = int(args[1])
        mystudentclass.put()
        return "Success"
    def removeClass(self, *args):
        if args[1]=='Student':
            myclass = model.StudentClasses.get_by_id(int(args[0]))
            myclass.key.delete()
            time.sleep(1)
            return "Done"
        myclass = model.TutorClasses.get_by_id(int(args[0]))
        myclass.key.delete()
        time.sleep(1)
        return "Done"
    def removeAvail(self, *args):
        avail = model.Availabilities.get_by_id(int(args[0]))
        avail.key.delete()
        time.sleep(1)
        return "Done"
    def addTutorClass(self, *args):
        myrate = 0
        try:
            myrate = float(args[2])
        except:
            return "Please select a valid hourly rate."
        try:
            query = "SELECT * FROM TutorClasses WHERE class_id = "+args[0]+" AND tutor = "+args[1]
            iterator = ndb.gql(query)
            for item in iterator:
                return "You are already offering this class."
            myclass = model.TutorClasses(
                class_id = int(args[0]),
                tutor = int(args[1]),
                rate = myrate)
            myclass.put()
            time.sleep(1)
            return "Success"
        except:
            return "We were unable to add your class. Please reload the page and try again."
    def addStudentClass(self, *args):
        try:
            query = "SELECT * FROM StudentClasses WHERE class_id = "+args[0]+" AND student = "+args[1]
            iterator = ndb.gql(query)
            for item in iterator:
                return "You are already taking this class."
            myclass = model.StudentClasses(
                class_id = int(args[0]),
                student = int(args[1]),
                status = 0)
            myclass.put()
            time.sleep(1)
            return "Success"
        except:
            return "We were unable to add your class. Please reload the page and try again."
    def searchClasses(self, *args):
        string = '<tr><td align="center">Course:</td><td align="center">Name:</td>'
        if args[2] == 'Tutor':
            string += '<td align="center">Rate:</td>'
        string +='<td align="center">Add:</td></tr>'
        department = args[0]
        courseno = -1
        args1 = ''
        try:
            args1 = args[1]
        except:
            args1 = ''
        if args1 == 'NULL':
            courseno = 0
        else:
            try:
                courseno = int(args1)
            except:
                return '<tr><td align="center">Please enter a valid course number.</td></tr>'
        query = ndb.gql("Select * from Settings")
        settings = None
        for item in query:
            settings = item
        query = "SELECT * FROM Classes"
        where = False
        if args[0] != "---":
            query += " WHERE department = '"+department+"'"
            where = True
        if courseno > 0 and courseno < 1000:
            query2 = " WHERE "
            if where:
                query2 = " AND "
            query += query2
            if courseno < 10:
                query += "coursenumber >= "+str(courseno)+"00 "
                query += "AND coursenumber <= "+str(courseno)+"99"
            elif courseno < 100:
                query += "coursenumber >= "+str(courseno)+"0 "
                query += "AND coursenumber <= "+str(courseno)+"9"
            else:
                query += "coursenumber = "+str(courseno)
        iterator = ndb.gql(query)
        string2 = ""
        disabled = ''
        if not(settings.tutorsetrate):
            disabled = ' disabled'
        for myclass in iterator:
            string2+='<tr><td align="center">'+myclass.department+" "+str(myclass.coursenumber)+"</td>"
            string2+='<td align="center">'+myclass.classname+"</td>"
            onclick = 'addStudentClass('+str(myclass.key.integer_id())+')'
            if args[2] == 'Tutor':
                string2+='<td align="center"><input id="rate'+str(myclass.key.integer_id())+'" value="'+au.moneyFormat(settings.tutorrate)+'" '+disabled+'/></td>'
                onclick = 'addTutorClass('+str(myclass.key.integer_id())+')'
            string2+='<td align="center"><button onclick="'+onclick+'">Add Course</button></td></tr>'
        if string2 == "":
            return '<tr><td align="center">Your query returned no results</td></tr>'
        return string+string2

class Checkout(webapp2.RequestHandler):
    def post(self):
        at = ""
        at = self.request.get('accesstoken',"")
        #raise Exception(len(at))
        if len(at) < 6:
            self.redirect('/error2.html')
        else:    
            amount = ""
            amount = self.request.get('amount',1)
            resp = ""
            resp = self.request.get('comment',"")
            myuid = ""
            myuid = self.request.get('userid',"")
            url = ""
            url = self.request.host+'/payappointment.html?appt='+self.request.get('appointment')+'&at='+at
            if(amount == ""):
                amount = 1
            if(resp == ""):
                resp = "TEST DESCRIPTION"
            mywepay = au.WePay(production, at)
            respon = au.makeCheckout(mywepay, myuid, amount, resp,'http://'+url)
            myson = json.loads(respon)

            #raise Exception('RESPONSE: '+respon)
            resp = myson['checkout_uri']
            template_values = {
                'logo': au.getLogo(),
                'emblem': au.getEmblem(),
                'checkout' : resp
            }
            template = JINJA_ENVIRONMENT.get_template('checkout.html')
            self.response.write(template.render(template_values))

class PayAppointment(webapp2.RequestHandler):
    def get(self):
        apptid = self.request.get('appt')
        appt = model.Appointments.get_by_id(int(apptid))
        if appt == None:
            self.redirect('/')
            return
        checkoutid = self.request.get('checkout_id')
        accesstoken = self.request.get('at')
        json = au.getpaymentinfo(checkoutid,accesstoken)
        if appt.cost == json['amount']:
            appt.paid = True
            appt.checkoutid = int(checkoutid)
            appt.put()
            template_values = {
            }
            template = JINJA_ENVIRONMENT.get_template('thankyou.html')
            self.response.write(template.render(template_values))
        else:
            self.redirect('/')

class UpdateHandler(webapp2.RequestHandler):
    def get(self):
        deferred.defer(model.UpdateSchema)
        self.response.out.write('Schema migration successfully initiated.')

class WepayAccountCreate(webapp2.RequestHandler):
    def get(self):
        template_values = {
        }
        template = JINJA_ENVIRONMENT.get_template('createaccount.html')
        self.response.write(template.render(template_values))


class CreateWepayAccount(webapp2.RequestHandler):
    def get(self):
        user = model.getUser(self.request.cookies.get('user',''),self.request.cookies.get('pass',''))
        # oauth2 parameters
        code = ''
        code = self.request.get('code',''); # the code parameter from step 2
        redirect_uri = "http://delaware.tutorsbin.com/"; # this is the redirect_uri you used in step 1
        if(code != ''):
            # create an account for a user
            resp = wepay.get_token(redirect_uri, client_id, client_secret, code)
            self.response.write(resp);
            mywepay = au.WePay(production, resp['access_token'])
            # create an account for a user
            response2 = mywepay.call('/account/create', {
                'name': user.fullname,
                'description': 'A payment account for Tutorsbin'
            })
            response2 = json.loads(response2)
            #raise Exception('RESPONSE: '+str(response2['account_id']))
            #self.response.out.write(str(response2))
        else:
            self.response.out.write('Error')
        user.wepayuid=str(response2['account_id'])
        user.wepayat =str(resp['access_token'])
        user.put()
app = webapp2.WSGIApplication([
    ('/', Landing),
    ('/calendar.html', Calendar),
    ('/myprofile.html', myprofile),
    ('/mytutors.html', mytutors),
    ('/mytutees.html', mytutees),
    ('/myresources.html', myresources),
    ('/tutorsearch.html',tutorsearch),
    ('/register.html', Register),
    ('/gensettings.html', GeneralSettings),
    ('/adminresources.html', AdminResources),
    ('/payappointment.html',PayAppointment),
    ('/groupcalendar.html', GroupCalendar),
    ('/mystudents.html', MyStudents),
    ('/error.html', Error),
    ('/error2.html', Error2),
    ('/paymentrequest.html',PaymentRequest),
    ('/createuser', CreateUser),
    ('/modifyuser', ModifyUser),
    ('/studentgrouppay',StudentGroupPay),
    ('/addTestData',AddTestData),
    ('/addAdminData',AddAdminData),
    ('/requestStudentGroup',RequestStudentGroup),
    ('/acceptStudent',AcceptStudent),
    ('/acceptTutor',AcceptTutor),
    ('/Denytutor',Denytutor),
    ('/cancelappointment',CancelAppointment),
    ('/login',LogIn),
    ('/logout',LogOut),
    ('/applyAsTutor',ApplyAsTutor),
    ('/addAvailability',AddAvailability),
    ('/sendRequest',SendRequest),
    ('/uploadPhoto',UploadPhoto),
    ('/uploadLogo',UploadLogo),
    ('/uploadEmblem',UploadEmblem),
    ('/uploadResource',UploadResource),
    ('/uploadStringResource',UploadStringResource),
    ('/viewPhoto/([^/]+)?',ViewPhotoHandler),
    ('/acceptRequest',AcceptRequest),
    ('/checkout.html',Checkout),
    ('/database',Database),
    ('/createaccount.html',WepayAccountCreate),
    ('/useraccountcreate',CreateWepayAccount),
    ('/managetutors.html',managetutors),
    ('/contactus.html',contactus),
    ('/GoonVacation',GoonVacation),
    ('/AcceptClass', AcceptClass),
    ('/DenyClass',DenyClass),
    ('/ChangeSetRate',ChangeSetRate),
    ('/SubmitRate',SubmitRate),
    ('/comebackfromvacation',comebackfromvacation),
    ('/tos.html',TOS),
    ('/reg.html',RegisterReplace),
    ('/sendm',sendmail),
    ('/update_schema', UpdateHandler)
], debug=True)
