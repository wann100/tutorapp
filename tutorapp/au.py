
from header import *
import json
import model

#function getdate
#MOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
#This functions take 5 strings pertaining to 1 "EVENT"
#in the fullcalendar.
#The dates are in ISO8601 format: (http://www.w3.org/TR/NOTE-datetime)
#YYYY-MM-DDThh:mm:ssTZD (eg 1997-07-16T19:20:30+01:00)
#Colors are in #fffff format.
def getdate(title,start,end,color,allDay):
    data = {'title': title,'start': start,'end': end,'color': color,'allDay': allDay}
    return json.dumps(data,separators=(',',':'))

#function makecalendar
#MOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
#This functions take an array of dates
#and returns a string tha can be inputed into fullcalendar
def makecalendar(*dates):
    mystring = ''
    for date in dates:
        mystring += date.__str__()
    print mystring
    return mystring

def getClassHTML(myclass,classnum,status,studentclassid):
    string = '<tr><td class="col_title">'
    if classnum == 1:
        string += 'Class Code'
    string += '</td><td></td>'
    string += '<td class="col_title">Class:</td><td></td>'
    string += '<td class="col_title">'
    if classnum == 1:
        string += 'Status'
    string += '</td><td class="col_title">Delete?</td>'
  #  string +='<td class="col_title">Rate/hour </td></tr>'
    string += '<tr><td class="class_code">'+myclass.department+' '+myclass.coursenumber.__str__()+'</td><td></td>'
    string += '<td class="class_name">'+myclass.classname+'</td><td></td>'
    string += '<td class="class_status">'
    string += '<select style="width:50px; height:90px;" name="'+str(studentclassid)+'" id="'+str(studentclassid)+'" onchange="updateStatus(\''+str(studentclassid)+'\');">'
    names = ['N','S','C']
    colors = ['gray','orange','blue']
    for i in range(3):
        string += '<option value="'+str(i)+'" '
        if i==status:
            string += 'selected="selected" '
        string += 'title="statics/images/status'+colors[i]+'.png">'+names[i]+'</option>'
    string += '</select></td><td class="class_status" align="center"><img class="del-class" onclick="changeDeleteClass('+str(studentclassid)+');" src="statics/images/minus.png" /></td></tr>'
    return string

def getTutorClassHTML(myclass,classnum,rate,tutorclassid):
    string = '<tr><td class="col_title">'
    if classnum == 1:
        string += 'Class Code'
    string += '</td><td></td>'
    string += '<td class="col_title">Class:</td><td></td>'
    string += '<td class="col_title">'
    if classnum == 1:
        string += 'Rate'
    string += '</td></tr>'
    string += '<tr><td class="class_code">'+myclass.department+' '+myclass.coursenumber.__str__()+'</td><td></td>'
    string += '<td class="class_name">'+myclass.classname+'</td><td></td>'
    string += '<td class="class_status">'+moneyFormat(rate)+'</td></tr>'
    return string


def moneyFormat(num):
    dollars = int(num)
    cents = int(num*100+.5-dollars*100)
    string = str(dollars)+"."
    if cents < 10:
        string += "0"
    return string + str(cents)

def formattime(time):
    string = str((time.hour-1)%12+1)+':'
    if time.minute < 10:
        string += '0'
    string += str(time.minute)
    if time.hour >= 12:
        return string+'pm'
    return string+'am'

def getRequestInfo(request):
    requestid = str(request.key.integer_id())
    student = model.Users.get_by_id(request.student)
    tutorclass = model.TutorClasses.get_by_id(request.tutorclassid)
    tutor = model.Users.get_by_id(tutorclass.tutor)
    myclass = model.Classes.get_by_id(tutorclass.class_id)
    majors = student.major1
    minors = student.minor1
    avatar = 'statics/images/profilepic.png'
    if student.avatar:
        avatar = '/viewPhoto/'+student.avatar.__str__()
    years = ['Freshman','Sophmore','Junior','Senior']
    string = '<table style="border:none; font-family:\'Kreon\'; padding-left:30px;">'
    string += '<td><table style="border: 2px solid black; border-collapse: collapse; font-family:\'Kreon\'; background:rgb(245,245,245); border-color:rgb(204,204,204);"><tr>'
    string += '<td style="width:400px; border-right:2px dashed rgb(204,204,204);">'
    string += '<div class="wrap" style="width:300px;">'
    string += '<div style="padding-left:15px; width:150px; font-size:80%; text-align:right;">'
    string += '<img width="75%" src="'+avatar+'" style="height: auto; width:150px; height:150px; " alt="alternate text" ></div>'
    string += '<p><span style="font-size:2em; font-weight:bold;">'
    string += '<span id="name'+requestid+'">'+student.fullname+'</span><br /></span><span style="font-size:0.9em;">'
    string += 'Status: Student <br />Year: <span id="year'+requestid+'">'+years[student.year-1]+'</span><br />'
    string += 'Major: <span id="major'+requestid+'">'+majors+'</span>'
    string += '<br />Minor: <span id="minor'+requestid+'">'+minors+'</span></span></p></div></td>'
    string += '<td style="padding: 15px; border-right:2px dashed rgb(204,204,204);"><p align="center">'
    string += '<span style="font-size:1.1em; font-weight:bold;">Dates and Times</span><br /></p>'
    string += '<p style="font-size:0.9em;">'
    requestlines = ndb.gql('SELECT * FROM RequestLines where requestid = '+requestid)
    for requestline in requestlines:
        start = requestline.start
        end = requestline.end
        string += str(start.month)+'/'+str(start.day)+'/'+str(start.year)+':<br />'
        string += formattime(start) + ' - '+formattime(end)+'<br/>'
    string += '</td><td style="padding: 15px;">'
    string += '<p align="center" style="margin-top:0px;"><span style="font-size:1.1em; font-weight:bold;">Requested Class</span><br /></p>'
    string += '<p style="font-size:0.8em;">'+myclass.department+' '+str(myclass.coursenumber)
    string += ': $'+moneyFormat(tutorclass.rate)+'/hr</p></td><td>'
    string += '<table border="0"><td><tr><p style="padding-left: 30px;">'
    string += '<span style="font-size:1.5em; font-weight:bold;">Notes:</span><br />'
    string += '<div id=\'tutornotes\'>'+request.notes+'</div></p>'
    string += '<center><form method="post" action="/acceptRequest">'
    string += '<input hidden name="requestid" value="'+requestid+'" />'
    string += '<input type="submit" id=\'acceptrequest\' value="ACCEPT REQUEST" />'
    string += '</form><br />'
    string += '<button id=\'declinerequest\'>DECLINE REQUEST</button>'
    string += '</center></tr><tr></tr></td></table>'
    string += '</td></tr></table></table>'
    return string

def getAppointmentInfo(appointment):
    tutorclassid = appointment.tutorclassid
    mytutorclass = model.TutorClasses.get_by_id(tutorclassid)
    myclass = model.Classes.get_by_id(mytutorclass.class_id)
    tutor = model.Users.get_by_id(mytutorclass.tutor)
    tutorid = str(tutor.key.integer_id())
    student = model.Users.get_by_id(appointment.student)
    majors = tutor.major1
    minors = tutor.minor1
    years = ['Freshman','Sophmore','Junior','Senior']
    avatar = 'statics/images/profilepic.png'
    if tutor.avatar:
        avatar = '/viewPhoto/'+tutor.avatar.__str__()
    string = '<table style="border:none; font-family:\'Kreon\'; padding-left:30px;">'
    string += '<td><table style="border: 2px solid black; border-collapse: collapse;width: 800px; font-family:\'Kreon\'; background:rgb(245,245,245); border-color:rgb(204,204,204);"><tr>'
    string += '<td style="width:400px; border-right:2px dashed rgb(204,204,204);">'

    string += '<div class="wrap" style="width:300px;">'
    string += '<div style="padding-left:15px; width:150px; font-size:80%; text-align:right;">'
    string += '<img id="avatar'+tutorid+'" width="75%" src="'+avatar+'" style="height: auto; width:150px; height:150px; " alt="alternate text" ></div>'
    string += '<p><span style="font-size:2em; font-weight:bold;">'
    string += '<span id="name'+tutorid+'">'+tutor.fullname+'</span><br /></span><span style="font-size:0.9em;">'
    string += 'Status: Tutor <br />Year: <span id="year'+tutorid+'">'+years[tutor.year-1]+'</span><br />'
    string += 'Major: <span id="major'+tutorid+'">'+majors+'</span>'
    string += '<br />Minor: <span id="minor'+tutorid+'">'+minors+'</span></span></p></div></td>'
    string += '<td style="padding: 15px; border-right:2px dashed rgb(204,204,204);"><p align="center">'
    string += '<span style="font-size:1.1em; font-weight:bold;">Appointment Date</span><br /></p>'
    string += '<p style="font-size:0.9em;">'
    daysofweek = ['Su','M','Tu','W','Th','F','Sa']
    datetimestring = str(appointment.start.month)+'-'+str(appointment.start.day)+'-'+str(appointment.start.year)+'<br/>'+formattime(appointment.start)+' - '+formattime(appointment.end)
    string += '<span id="avail'+tutorid+'">'+datetimestring+'</span></td><td style="padding: 15px;">'
    string += '<p align="center" style="margin-top:0px;"><span style="font-size:1.1em; font-weight:bold;">Appointment Class</span><br /></p>'
    string += '<p style="font-size:0.8em;">'
    string += myclass.department+' '+str(myclass.coursenumber)+': $'+moneyFormat(appointment.cost)+'</p>'
    string += '<form method="post" action="checkout.html"/>'
    string += '<input hidden name="amount" value="'+str(appointment.cost)+'" />'
    string += '<input hidden name="comment" value="Payment of $'+moneyFormat(appointment.cost)+' to '+tutor.fullname+' for '+myclass.department+' '+str(myclass.coursenumber)+' by '+student.fullname+'." />'
    string += '<input hidden name="accesstoken" value="'+tutor.wepayat+'" />'
    string += '<input hidden name="userid" value='+tutor.wepayuid+' />'
    string += '<input hidden name="appointment" value='+str(appointment.key.integer_id())+' />'
    string += '<div ><a style="text-decoration:none;"><input type="submit" id="tutorbutton" value="PAY NOW" style="background-color: #00C100;" /></a>'

    hasStudentGroup = False
    query = ndb.gql("SELECT * FROM StudentGroups WHERE student = "+str(student.key.integer_id()))
    for item in query:
        hasStudentGroup = True
    if hasStudentGroup:
        string += '<div ><a style="text-decoration:none;"><input type="button" class="sponpay" value="Sponsor PAY" onclick="document.getElementById(\'studentgroupapptid\').value = \''+str(appointment.key.integer_id())+'\';" style="background-color: #00C100;" /></a>'
    if appointment.paid == False:
        string +='<div class="cancelbutton"><button style="cursor:pointer;display:inline; color: white; background-color:black; border: 0; margin: 0; height: 20px; width: 200px; font-weight: bold; font-size:0.9em;">CANCEL</button></div>'
    string+='<br/><center>or'
    string+='<br/>Bring Cash/Check</center> </div>'
    string += '</form>'
    string += '</td></tr></table></td><td>'
    string += '<table style="border:none; font-family:\'Kreon\';">'
    string += '<td style="border:none; padding: 15px; padding-left:30px;">'
    string += '<p style="margin-top:-75px;"><span style="font-size:1.5em; font-weight:bold;">Notes:</span><br />'
    string += '<span style="font-size:0.9em;">'+tutor.aboutme+'</span>'
    string += '</p></td></table></table>'
    return string

def tutorApprovedAppointment(appointment):
    tutorclassid = appointment.tutorclassid
    mytutorclass = model.TutorClasses.get_by_id(tutorclassid)
    myclass = model.Classes.get_by_id(mytutorclass.class_id)
    student = model.Users.get_by_id(appointment.student)
    studentid = str(appointment.student)
    tutor = model.Users.get_by_id(mytutorclass.tutor)
    tutorid = str(tutor.key.integer_id())
    student = model.Users.get_by_id(appointment.student)
    majors = student.major1
    minors = student.minor1
    years = ['Freshman','Sophmore','Junior','Senior']
    avatar = 'statics/images/profilepic.png'
    if student.avatar:
        avatar = '/viewPhoto/'+student.avatar.__str__()
    string = '<table style="border:none; font-family:\'Kreon\'; padding-left:30px;">'
    string += '<td><table style="border: 2px solid black; border-collapse: collapse;width: 800px; font-family:\'Kreon\'; background:rgb(245,245,245); border-color:rgb(204,204,204);"><tr>'
    string += '<td style="width:400px; border-right:2px dashed rgb(204,204,204);">'

    string += '<div class="wrap" style="width:300px;">'
    string += '<div style="padding-left:15px; width:150px; font-size:80%; text-align:right;">'
    string += '<img id="avatar'+studentid+'" width="75%" src="'+avatar+'" style="height: auto; width:150px; height:150px; " alt="alternate text" ></div>'
    string += '<p><span style="font-size:2em; font-weight:bold;">'
    string += '<span id="name'+studentid+'">'+student.fullname+'</span><br /></span><span style="font-size:0.9em;">'
    string += 'Status: Student <br />Year: <span id="year'+studentid+'">'+years[student.year-1]+'</span><br />'
    string += 'Major: <span id="major'+studentid+'">'+majors+'</span>'
    string += '<br />Minor: <span id="minor'+studentid+'">'+minors+'</span></span></p></div></td>'
    string += '<td style="padding: 15px; border-right:2px dashed rgb(204,204,204);"><p align="center">'
    string += '<span style="font-size:1.1em; font-weight:bold;">Appointment Date</span><br /></p>'
    string += '<p style="font-size:0.9em;">'
    daysofweek = ['Su','M','Tu','W','Th','F','Sa']
    datetimestring = str(appointment.start.month)+'-'+str(appointment.start.day)+'-'+str(appointment.start.year)+'<br/>'+formattime(appointment.start)+' - '+formattime(appointment.end)
    string += '<span id="avail'+tutorid+'">'+datetimestring+'</span></td><td style="padding: 15px;">'
    string += '<p align="center" style="margin-top:0px;"><span style="font-size:1.1em; font-weight:bold;">Appointment Class</span><br /></p>'
    string += '<p style="font-size:0.8em;">'
    string += myclass.department+' '+str(myclass.coursenumber)+': $'+moneyFormat(appointment.cost)+'</p>'
    string += '<form method="post" action="checkout.html"/>'
    string += '<input hidden name="amount" value="'+str(appointment.cost)+'" />'
    string += '<input hidden name="comment" value="Payment of $'+moneyFormat(appointment.cost)+' to '+tutor.fullname+' for '+myclass.department+' '+str(myclass.coursenumber)+' by '+student.fullname+'." />'
    string += '<input hidden name="accesstoken" value="'+tutor.wepayat+'" />'
    string += '<input hidden name="userid" value='+tutor.wepayuid+' />'
    string += '<input hidden name="appointment" value='+str(appointment.key.integer_id())+' />'
    string += '<div ><p style="background-color:orange;padding-left: 50px;padding-right: 43px;color:white;">APPROVED</p>'
    string +='<div class="cancelbutton"><button style="cursor:pointer;display:inline; color: white; background-color:black; border: 0; margin: 0; height: 20px; width: 200px; font-weight: bold; font-size:0.9em;" onclick="document.getElementById(\'cancelapptid\').value = \''+str(appointment.key.integer_id())+'\';">CANCEL</button></div>'
    string+='<br/><center>or'
    string+='<br/>Bring Cash/Check</center> </div>'
    string += '</form>'
    string += '</td></tr></table></td><td>'
    string += '<table style="border:none; font-family:\'Kreon\';">'
    string += '<td style="border:none; padding: 15px; padding-left:30px;">'
    string += '<p style="margin-top:-75px;"><span style="font-size:1.5em; font-weight:bold;">Notes:</span><br />'
    string += '<span style="font-size:0.9em;">'+student.aboutme+'</span>'
    string += '</p></td></table></table>'
    return string

def getGroupAppointmentInfo(appointment):
    tutorclassid = appointment.tutorclassid
    mytutorclass = model.TutorClasses.get_by_id(tutorclassid)
    myclass = model.Classes.get_by_id(mytutorclass.class_id)
    tutor = model.Users.get_by_id(mytutorclass.tutor)
    tutorid = str(tutor.key.integer_id())
    studentid = str(appointment.student)
    student = model.Users.get_by_id(appointment.student)
    majors = tutor.major1
    minors = tutor.minor1
    years = ['Freshman','Sophmore','Junior','Senior']
    avatar = 'statics/images/profilepic.png'
    if student.avatar:
        avatar = '/viewPhoto/'+student.avatar.__str__()
    string = '<table style="border:none; font-family:\'Kreon\'; padding-left:30px;">'
    string += '<td><table style="border: 2px solid black; border-collapse: collapse; width: 800px;font-family:\'Kreon\'; background:rgb(245,245,245); border-color:rgb(204,204,204);"><tr>'
    string += '<td style="width:400px; border-right:2px dashed rgb(204,204,204);">'

    string += '<div class="wrap" style="width:300px;">'
    string += '<div style="padding-left:15px; width:150px; font-size:80%; text-align:right;">'
    string += '<img id="avatar'+studentid+'" width="75%" src="'+avatar+'" style="height: auto; width:150px; height:150px; " alt="alternate text" ></div>'
    string += '<p><span style="font-size:2em; font-weight:bold;">'
    string += '<span id="name'+studentid+'">'+student.fullname+'</span><br /></span><span style="font-size:0.9em;">'
    string += 'Tutor: '+tutor.fullname+'<br />'
    string += '</p></div></td>'
    string += '<td style="padding: 15px; border-right:2px dashed rgb(204,204,204);"><p align="center">'
    string += '<span style="font-size:1.1em; font-weight:bold;">Appointment Date</span><br /></p>'
    string += '<p style="font-size:0.9em;">'
    daysofweek = ['Su','M','Tu','W','Th','F','Sa']
    datetimestring = str(appointment.start.month)+'-'+str(appointment.start.day)+'-'+str(appointment.start.year)+'<br/>'+formattime(appointment.start)+' - '+formattime(appointment.end)
    string += '<span id="avail'+tutorid+'">'+datetimestring+'</span></td><td style="padding: 15px;">'
    string += '<p align="center" style="margin-top:0px;"><span style="font-size:1.1em; font-weight:bold;">Appointment Class</span><br /></p>'
    string += '<p style="font-size:0.8em;">'
    string += myclass.department+' '+str(myclass.coursenumber)+': $'+moneyFormat(appointment.cost)+'</p>'
    string += '<form method="post" action="checkout.html"/>'
    string += '<input hidden name="amount" value="'+str(appointment.cost)+'" />'
    string += '<input hidden name="comment" value="Payment of $'+moneyFormat(appointment.cost)+' to '+tutor.fullname+' for '+myclass.department+' '+str(myclass.coursenumber)+' by '+student.fullname+'." />'
    string += '<input hidden name="accesstoken" value="'+tutor.wepayat+'" />'
    string += '<input hidden name="userid" value='+tutor.wepayuid+' />'
    string += '<input hidden name="appointment" value='+str(appointment.key.integer_id())+' />'
    string += '<div ><a style="text-decoration:none;"><input type="submit" id="tutorbutton" value="PAY NOW" style="background-color: #00C100;" /></a>'

    string += '</div></form></td></tr></table></td><td>'
    string += '<table style="border:none; font-family:\'Kreon\';">'
    string += '<td style="border:none; padding: 15px; padding-left:30px;">'
    string += '<p style="margin-top:-75px;"><br />'
    string += '</p></td></table></table>'
    return string

def getPendingInfo(appointment):
    tutorclassid = appointment.tutorclassid
    mytutorclass = model.TutorClasses.get_by_id(tutorclassid)
    myclass = model.Classes.get_by_id(mytutorclass.class_id)
    tutor = model.Users.get_by_id(mytutorclass.tutor)
    tutorid = str(tutor.key.integer_id())
    student = model.Users.get_by_id(appointment.student)
    majors = tutor.major1
    minors = tutor.minor1
    years = ['Freshman','Sophmore','Junior','Senior']
    avatar = 'statics/images/profilepic.png'
    if tutor.avatar:
        avatar = '/viewPhoto/'+tutor.avatar.__str__()
    string = '<table style="border:none; font-family:\'Kreon\'; padding-left:30px;">'
    string += '<td><table style="border: 2px solid black; border-collapse: collapse;width: 800px; font-family:\'Kreon\'; background:rgb(245,245,245); border-color:rgb(204,204,204);"><tr>'
    string += '<td style="width:400px; border-right:2px dashed rgb(204,204,204);">'

    string += '<div class="wrap" style="width:300px;">'
    string += '<div style="padding-left:15px; width:150px; font-size:80%; text-align:right;">'
    string += '<img id="avatar'+tutorid+'" width="75%" src="'+avatar+'" style="height: auto; width:150px; height:150px; " alt="alternate text" ></div>'
    string += '<p><span style="font-size:2em; font-weight:bold;">'
    string += '<span id="name'+tutorid+'">'+tutor.fullname+'</span><br /></span><span style="font-size:0.9em;">'
    string += 'Status: Tutor <br />Year: <span id="year'+tutorid+'">'+years[tutor.year-1]+'</span><br />'
    string += 'Major: <span id="major'+tutorid+'">'+majors+'</span>'
    string += '<br />Minor: <span id="minor'+tutorid+'">'+minors+'</span></span></p></div></td>'
    string += '<td style="padding: 15px; border-right:2px dashed rgb(204,204,204);"><p align="center">'
    string += '<span style="font-size:1.1em; font-weight:bold;">Appointment Date</span><br /></p>'
    string += '<p style="font-size:0.9em;">'
    daysofweek = ['Su','M','Tu','W','Th','F','Sa']
    datetimestring = str(appointment.start.month)+'-'+str(appointment.start.day)+'-'+str(appointment.start.year)+'<br/>'+formattime(appointment.start)+' - '+formattime(appointment.end)
    string += '<span id="avail'+tutorid+'">'+datetimestring+'</span></td><td style="padding: 15px;">'
    string += '<p align="center" style="margin-top:0px;"><span style="font-size:1.1em; font-weight:bold;">Appointment Class</span><br /></p>'
    string += '<p style="font-size:0.8em;">'
    string += myclass.department+' '+str(myclass.coursenumber)+': $'+moneyFormat(appointment.cost)+'</p>'
    string += '<form method="post" action="checkout.html"/>'
    string += '<input hidden name="amount" value="'+str(appointment.cost)+'" />'
    string += '<input hidden name="comment" value="Payment of $'+moneyFormat(appointment.cost)+' to '+tutor.fullname+' for '+myclass.department+' '+str(myclass.coursenumber)+' by '+student.fullname+'." />'
    string += '<input hidden name="accesstoken" value="'+tutor.wepayat+'" />'
    string += '<input hidden name="userid" value='+tutor.wepayuid+' />'
    string += '<input hidden name="appointment" value='+str(appointment.key.integer_id())+' />'
    string += '<div ><h1 style="background-color:orange;padding-left: 50px;padding-right: 43px;color:white;">Pending</h1>'
    string+=' </div>'
    string += '</form>'
    string += '</td></tr></table></td><td>'
    string += '<table style="border:none; font-family:\'Kreon\';">'
    string += '<td style="border:none; padding: 15px; padding-left:30px;">'
    string += '<p style="margin-top:-75px;"><span style="font-size:1.5em; font-weight:bold;">Notes:</span><br />'
    string += '<span style="font-size:0.9em;">'+tutor.aboutme+'</span>'
    string += '</p></td></table></table>'
    return string

def getTutorSearchInfo(tutor):
    tutorid = str(tutor.key.integer_id())
    majors = tutor.major1
    minors = tutor.minor1
    years = ['Freshman','Sophmore','Junior','Senior']
    avatar = 'statics/images/profilepic.png'
    if tutor.avatar:
        avatar = '/viewPhoto/'+tutor.avatar.__str__()
    string = '<table style="border:none; font-family:\'Kreon\'; padding-left:30px;">'
    string += '<td><table style="border: 2px solid black; border-collapse: collapse;width: 800px; font-family:\'Kreon\'; background:rgb(245,245,245); border-color:rgb(204,204,204);"><tr>'
    string += '<td style="width:400px; border-right:2px dashed rgb(204,204,204);">'

    string += '<div class="wrap" style="width:300px;">'
    string += '<div style="padding-left:15px; width:150px; font-size:80%; text-align:right;">'
    string += '<img id="avatar'+tutorid+'" width="75%" src="'+avatar+'" style="height: auto; width:150px; height:150px; " alt="alternate text" ></div>'
    string += '<p><span style="font-size:2em; font-weight:bold;">'
    string += '<span id="name'+tutorid+'">'+tutor.fullname+'</span><br /></span><span style="font-size:0.9em;">'
    string += 'Status: Tutor <br />Year: <span id="year'+tutorid+'">'+years[tutor.year-1]+'</span><br />'
    string += 'Major: <span id="major'+tutorid+'">'+majors+'</span>'
    string += '<br />Minor: <span id="minor'+tutorid+'">'+minors+'</span></span></p></div></td>'
    string += '<td style="padding: 15px; border-right:2px dashed rgb(204,204,204);"><p align="center">'
    string += '<span style="font-size:1.1em; font-weight:bold;">Availability</span><br /></p>'
    string += '<p style="font-size:0.9em;">'
    avails = ndb.gql('SELECT * FROM Availabilities WHERE user = '+str(tutor.key.integer_id()))
    availstring = ''
    daysofweek = ['Su','M','Tu','W','Th','F','Sa']
    for avail in avails:
        if availstring != '':
            availstring += '<br />'
        availstring += daysofweek[avail.dayofweek]+': '+formattime(avail.start)+'-'+formattime(avail.end)
    string += '<span id="avail'+tutorid+'">'+availstring+'</span></td><td style="padding: 15px;">'
    string += '<p align="center" style="margin-top:0px;"><span style="font-size:1.1em; font-weight:bold;">Current Classes</span><br /></p>'
    string += '<p style="font-size:0.8em;">'
    classlist = ndb.gql("select * from TutorClasses where tutor = "+tutorid)
    hiddenstr = '<span hidden id="classes'+tutorid+'">'
    onclick = 'ratesperclass = [];'
    for mytutorclass in classlist:
        myclass = model.Classes.get_by_id(mytutorclass.class_id)
        string += myclass.department + ' ' + str(myclass.coursenumber) +': '
        string += '$' + moneyFormat(mytutorclass.rate) + '/hr <br />'
        hiddenstr += '<option value="'+str(mytutorclass.key.integer_id())+'">'+myclass.department + ' ' + str(myclass.coursenumber)+'</option>'
        onclick += 'ratesperclass.push(['+str(mytutorclass.key.integer_id())+','+str(mytutorclass.rate)+']);'
    onclick += 'updateRequestForm('+tutorid+');'
    string += hiddenstr + '</span>'
    string += '</p><div class="contactbutton"><button id="tutorbutton" onclick="updateEmail(\''+tutor.email+'\')">CONTACT</button></div>'
    string += '</p><div class="requestbutton"><button id="tutorbutton" onclick="'+onclick+'">REQUEST</button></div>'
    string += '</td></tr></table></td><td>'
    #CHANGE THIS LINE TO WORK AND OPEN UP THEIR INBOX TO THEIR EMAIL INSTEAD OF ANOTHER REQUEST FORM;
    string += '<table style="border:none; font-family:\'Kreon\';">'
    string += '<td style="border:none; padding: 15px; padding-left:30px;">'
    string += '<p style="margin-top:-75px;"><span style="font-size:1.5em; font-weight:bold;">Notes:</span><br />'
    string += '<span style="font-size:0.9em;">'+tutor.aboutme+'</span>'
    string += '</p></td></table></table>'
    return string

def getCalendarFromAvailability(avail):
    string = "{'title':'Test','start':'"+ISO8601(avail.start)
    string +="','end':'"+ISO8601(avail.end)+"','color':'blue'},"
    return string

def getCalendarFromStudentAppointment(appoint):
    tutorclass = model.TutorClasses.get_by_id(appoint.tutorclassid)
    myclass = model.Classes.get_by_id(tutorclass.class_id)
    tutor = model.Users.get_by_id(tutorclass.tutor)
    color = 'blue'
    if appoint.paid:
        color = 'green'
    title = 'Appointment with '+tutor.fullname+' for '+myclass.department+' '+str(myclass.coursenumber)
    string = "{'title':'"+title+".','start':'"+ISO8601(appoint.start)
    string +="','end':'"+ISO8601(appoint.end)+"','color':'"+color+"'},"
    return string

def getCalendarFromTutorAppointment(appoint):
    tutorclass = model.TutorClasses.get_by_id(appoint.tutorclassid)
    myclass = model.Classes.get_by_id(tutorclass.class_id)
    student = model.Users.get_by_id(appoint.student)
    color = 'blue'
    if appoint.paid:
        color = 'green'
    title = 'Appointment with '+student.fullname+' for '+myclass.department+' '+str(myclass.coursenumber)
    string = "{'title':'"+title+".','start':'"+ISO8601(appoint.start)
    string +="','end':'"+ISO8601(appoint.end)+"','color':'"+color+"'},"
    return string

def getStudentGroupRequestForm(request):
    string = ' <tr><td class="info_fields">'
    string += '<form method="post" action="/acceptStudent">'
    student = model.Users.get_by_id(request.student)
    string += student.fullname+': '+student.email
    string += '<input name="id" value="'+str(request.key.integer_id())+'" hidden/>'
    string += '<input class="myinput" type="submit" value="Accept" /></form><br /></td><tr>'
    return string

def ISO8601(mydatetime):
    string = str(mydatetime.year) + '-'
    if mydatetime.month < 10:
        string += '0'
    string += str(mydatetime.month) + '-'
    if mydatetime.day < 10:
        string += '0'
    string += str(mydatetime.day) + 'T'
    if mydatetime.hour < 10:
        string+='0'
    string += str(mydatetime.hour)+':'
    if mydatetime.minute < 10:
        string+='0'
    return string + str(mydatetime.minute)+':00-05:00'

def getLogo():
    query = ndb.gql("Select * from Settings")
    settings = None
    for item in query:
        settings = item
    if not(settings.logo):
        return '../statics/images/university_logo.png'
    return '/viewPhoto/'+str(settings.logo)
def gettime():

    query = ndb.gql("Select * from Settings")
    settings = None
    for item in query:
        settings = item
    return str(settings.time)


def printfuturtutors(student):
    requestid = str(student.key.integer_id())
    string=''
    avatar=''
    if student.avatar:
        avatar = '/viewPhoto/'+student.avatar.__str__()
    string+='<table style="border:none; font-family:'"Kreon"'; padding-left:30px;">'
    string+= '<td>'
    string+= '<table style="border: 2px solid black; border-collapse: collapse; font-family:'"Kreon"'; background:rgb(245,245,245); border-color:rgb(204,204,204);">'
    string+= '<tr>'
    string+= '<td style="width:400px; border-right:2px dashed rgb(204,204,204);">'
    string+= '<div class="wrap" style="width:300px;">'
    string+='<div style="padding-left:15px; width:150px; font-size:80%; text-align:right;">'
    string+= '<img width="75%" src="'+avatar+'" style="height: auto; width:150px; height:150px;" alt="alternate text" >'
    string+= '</div>'
    string+= ' <p><span style="font-size:2em; font-weight:bold;">'
    string+= ' '+student.fullname+'<br /></span>'
    string+= '<span style="font-size:0.9em;">'
    string+= 'Status:Student <br />'
    string+= 'Year:"'+str(student.year)+'" <br />'
    string+= 'Major:"'+student.major1+'" <br />'
    string+= 'Email:"'+student.email+'" <br />'
    string+= ' Minor:"'+student.minor1+'"</span></p>'
    string+= '</div>'
    string+= '</td>'
    string+= '<td style="padding: 15px;">'
    string+= '<table width="100%" border="0" cellspacing="0" cellpadding="0"> <td> Would like to be a tutor </td>'
    string+= '<tr>'
    string+= ' <td><center>'
    string += '<center><form method="post" action="/acceptTutor">'
    string += '<input hidden name="requestid" value="'+requestid+'" />'
    string += '<input class="bluebutton" type="submit" id=\'accepttutor\' value="ACCEPT REQUEST" />'
    string += '</form><br />'
    string+= '<form method="post" action="/Denytutor">'
    string += '<input hidden name="requestid" value="'+requestid+'" />'
    string += '<button type="submit" id=\'declinerequest\'>DECLINE REQUEST</button>'
    string+=  '</form>'
    string+= ' </center></td>'
    string+= ' </tr>'
    string+= '</table> </td></tr></table></td> <td><table border="0"> <td><tr></tr></td></table></td></table>'
    return string
#####################################################################333
def printstudentsetrate(settings):
    string=''
    if (settings.tutorsetrate == True):
        string='checked'

    return string

def printrequestedclasses(requestedclass):
    string =''
    requestid = str(requestedclass.tutor)
    requestedclass = requestedclass.class_id
    classname=''
    query= ndb.gql("SELECT * FROM Users")
    classes = ndb.gql("SELECT * FROM Classes")
    for Classes in classes:
                classname =Classes.get_by_id(requestedclass).department + str(Classes.get_by_id(requestedclass).coursenumber)
#  string= str(requestid)
    avatar=''
    #student=''
    for Users in query:
     if(str(Users.key.integer_id()) ==requestid):

            student = Users
            if Users.avatar:
                avatar = '/viewPhoto/'+student.avatar.__str__()
            string+='<table style="border:none; font-family:'"Kreon"'; padding-left:30px;">'
            string+= '<td>'
            string+= '<table style="border: 2px solid black; border-collapse: collapse; font-family:'"Kreon"'; background:rgb(245,245,245); border-color:rgb(204,204,204);">'
            string+= '<tr>'
            string+= '<td style="width:400px; border-right:2px dashed rgb(204,204,204);">'
            string+= '<div class="wrap" style="width:300px;">'
            string+='<div style="padding-left:15px; width:150px; font-size:80%; text-align:right;">'
            string+= '<img width="75%" src="'+avatar+'" style="height: auto; width:150px; height:150px;" alt="alternate text" >'
            string+= '</div>'
            string+= ' <p><span style="font-size:2em; font-weight:bold;">'
            string+= ' '+student.fullname+'<br /></span>'
            string+= '<span style="font-size:0.9em;">'
            string+= 'Status:Student <br />'
            string+= 'Year:"'+str(student.year)+'" <br />'
            string+= 'Major:"'+student.major1+'" <br />'
            string+= 'Email:"'+student.email+'" <br />'
            string+= ' Minor:"'+student.minor1+'"</span></p>'
            string+= '</div>'
            string+= '</td>'
            string+= '<td style="padding: 15px;">'
            string+= '<table width="100%" border="0" cellspacing="0" cellpadding="0"> <td> <center>Would like to add:</center> </td>'
            string+= '<tr><td><center>'+str(classname)+'</center></td></tr>'
        #################for loop here and find the class and put it up
            string+= '<tr>'
            string+= ' <td><center>'
            string += '<center><form method="post" action="/AcceptClass">'
            string += '<input hidden name="requestid" value="'+requestid+'" />'
            string += '<input class="bluebutton" type="submit" id=\'AcceptClass\' value="ACCEPT REQUEST" />'
            string += '</form>'
            string+= '<form method="post" action="/DenyClass">'
            string += '<input hidden name="requestid" value="'+requestid+'" />'
            string += '<button type="submit" id=\'declinerequest\'>DECLINE REQUEST</button>'
            string+=  '</form>'
            string+= ' </center></td>'
            string+= ' </tr>'
            string+= '</table> </td></tr></table></td> <td><table border="0"> <td><tr></tr></td></table></td></table>'
    return string
###############################################################################################################
def getEmblem():
    query = ndb.gql("Select * from Settings")
    settings = None
    for item in query:
        settings = item
    if not(settings.emblem):
        return '../statics/images/symbol.png'
    return '/viewPhoto/'+str(settings.emblem)

#makeCheckout(wepayclass, number, number, string,redirect_url-string-)
def makeCheckout(wepay,account_id,amount,note,redirect_url):
    # create the checkout
    response = wepay.call('/checkout/create', {
        'account_id': account_id,
        'amount': amount,
        'short_description': note,
        'type': 'DONATION',
        'redirect_uri':redirect_url,
        'mode':'iframe'
    })
    return response

def getCheckout(checkout_id):
    response = wepay.call('/checkout', {
        'checkout_id': checkout_id
    })
    return response

def refund(checkout_id,at):
    mywepay = WePay(False, at)
    response = mywepay.call('/checkout/refund', {
        'checkout_id': str(checkout_id),
        'refund_reason': 'Refunded through Tutorsbin'
    })
    resp = str(response)
    count = resp.count('error')
    if(count > 0):
        return "Error"
    return response

def wepayinformation(user):
    string =' <tr> <td>Wepay Information:</td> </tr>'
   # string+= '<tr> <td class="info_fields"><input value="'+str(user.wepayaccount)+'"/></td> </tr>'
   # string+= '<tr> <td class="info_fields"><input value="'+str(user.wepaycheckout)+'"/></td></tr>'
    string+= '<tr><td width=10% colspan="1"><a id="start_oauth2">Click here to create your WePay account</a> </td></tr>'
    return string

def getpaymentinfo(checkout_id,at):
    mywepay = WePay(False, at)
    response = mywepay.call('/checkout', {
        'checkout_id': checkout_id
    })
    return json.loads(response)

#WEPAY STUFF ====================================================================================
#================================================================================================
class WePay(object):

    """
    A client for the WePay API.
    """

    def __init__(self, production=True, access_token=None, api_version=None):
        """
        :param bool production: When ``False``, the ``stage.wepay.com`` API
            server will be used instead of the default production.
        :param str access_token: The access token associated with your
            application.
        """
        self.access_token = access_token
        self.api_version = api_version

        if production:
            self.api_endpoint = "https://wepayapi.com/v2"
            self.browser_endpoint = "https://www.wepay.com/v2"
        else:
            self.api_endpoint = "https://stage.wepayapi.com/v2"
            self.browser_endpoint = "https://stage.wepay.com/v2"

    def call(self, uri, params=None, token=None):
        """
        Calls wepay.com/v2/``uri`` with ``params`` and returns the JSON
        response as a python dict. The optional token parameter will override
        the instance's access_token if it is set.

        :param str uri: The URI on the API endpoint to call.
        :param dict params: The parameters to pass to the URI.
        :param str token: Optional override for this ``WePay`` object's access
            token.
        """

        headers = {'Content-Type': 'application/json',
                   'User-Agent': 'WePay Python SDK'}
        url = self.api_endpoint + uri

        if self.access_token or token:
            headers['Authorization'] = 'Bearer ' + \
                (token if token else self.access_token)

        if self.api_version:
            headers['Api-Version'] = self.api_version

        if params:
            params = json.dumps(params)
        
        try:
            response = urlfetch.fetch(
                url=url,payload=params, method=urlfetch.POST,headers=headers)
            return response.content          
        except:
            if 400 <= response.status_code <= 599:
                raise Exception('Unknown error. Please contact support@wepay.com '+response.content)

    def get_token(self, redirect_uri, client_id, client_secret, code, callback_uri=None):
        """
        Calls wepay.com/v2/oauth2/token to get an access token. Sets the
        access_token for the WePay instance and returns the entire response
        as a dict. Should only be called after the user returns from being
        sent to get_authorization_url.
        :param str redirect_uri: The same URI specified in the
        :py:meth:`get_authorization_url` call that preceeded this.
        :param str client_id: The client ID issued by WePay to your app.
        :param str client_secret: The client secret issued by WePay
        to your app.
        :param str code: The code returned by :py:meth:`get_authorization_url`.
        :param str callback_uri: The callback_uri you want to receive IPNs for
        this user on.
        """
        params = {
            'redirect_uri': redirect_uri,
            'client_id': client_id,
            'client_secret': client_secret,
            'code': code,
        }
        #response = 'client_id : '+str(client_id)
        if callback_uri:
            params.update({'callback_uri': callback_uri})
        response = self.call('/oauth2/token', params)
        #self.access_token = response['access_token']
        return json.loads(response)


def sendmessage(recipient, subject, message):
    if isinstance(recipient, model.Users):
        sendmessage(recipient.fullname+' <'+recipient.email+'>',subject,message)
        return
    mail.send_mail(
        "Continuous Software Solutions <mamadouwann@gmail.com>",
        recipient,
        subject,
        message)
def vacationbutton(student):
    string=''
    if (student.available):
       string+= '<a id="add-avail" style="display:inline-block; margin-left: 50px; text-decoration:none; font-size: 0.85em;" href=""><img class="plus" src="statics/images/plus.png" />&nbsp;ADD AVAILABILITY</a>'
       string+='<form method="get"action="/GoonVacation">'
       string+='<input class="bluebutton" type="submit" id='"+GoonVacation+"' value="Go On Vacation" />'
       string+= '</form>  <div id="informationbutton"><button style="font-family:"Arvo"; font-size:1.0em "><img src="statics/icons/icon_faq.gif"/></button></div></td>'
    else:
       string+='<form method="get"action="/comebackfromvacation">'
       string+='<input class ="bluebutton" type="submit" id='"+comebackfromvacation+"' value="Come back from vacation" />'
       string+= '</form><div id="informationbuttontwo"><button style="font-family:"Arvo"; font-size:1.0em "><img src="statics/icons/icon_faq.gif"/></button></div>'

    return string
