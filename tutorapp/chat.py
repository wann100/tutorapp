#!/usr/bin/env python
"""
	The Chat Handlers
	
	Copyright 2010 Netgamix LLC
	License: http://netgamix.com/information/terms/
	
"""

import header


class MainHandler(webapp.RequestHandler):
	def get(self):
		self.session = Session()
		error = self.session['error'] if 'error' in self.session else ""
		template_vars={'error':error}
		temp = os.path.join(os.path.dirname(__file__),'templates/main.html')
		outstr = template.render(temp, template_vars)
		self.response.out.write(outstr)
		
class ChatHandler(webapp.RequestHandler):
	def get(self):
		self.redirect('/')
		
	def post(self):
		# Some session from http://gaeutilities.appspot.com/
		self.session = Session()
		# obtain the nick
		nick = self.request.get('nick')
		if not nick:
			self.redirect('/')
		# check if a user with that nick already exists
		user = OnlineUser.all().filter('nick =', nick).get()
		if user:
			self.session['error']='That nickname is taken'
			self.redirect('/')
			return
		else:
			self.session['error']=''
		# generate a unique id for the channel api
		channel_id=str(uuid.uuid4())
		chat_token = channel.create_channel(channel_id)
		# save the user
		user = model.OnlineUser(nick=nick,channel_id=channel_id)
		user.put()
		# obtain all the messages
		messages=model.Message.all().order('date').fetch(1000)
		# generate the template and answer back to the user
		template_vars={'nick':nick,'messages':messages,'channel_id':channel_id,'chat_token':chat_token}
		temp = os.path.join(os.path.dirname(__file__),'templates/chat.html')
		outstr = template.render(temp, template_vars)
		self.response.out.write(outstr)
		
		
class NewMessageHandler(webapp.RequestHandler):	
	def post(self):
		# Get the parameters		
		text = self.request.get('text')
		channel_id = self.request.get('channel_id')		
		q = db.GqlQuery("SELECT * FROM OnlineUser WHERE channel_id = :1", channel_id)
		nick = q.fetch(1)[0].nick	
		date = datetime.datetime.now()
		message=model.Message(user=nick,text=strip_tags(text), date = date, date_string = date.strftime("%H:%M:%S"))
		message.put()
		# Generate the template with the message
		messages=[message]
		template_vars={'messages':messages}
		temp = os.path.join(os.path.dirname(__file__),'templates/messages.html')
		outstr = template.render(temp, template_vars)
		channel_msg = json.dumps({'success':True,"html":outstr})
		# Send the message to all the connected users
		users = model.OnlineUser.all().fetch(100)		
		for user in users:						
			channel.send_message(user.channel_id, channel_msg)	      
		
class ClearDBHandler(webapp.RequestHandler):	
	def get(self):
		q = OnlineUser.all().filter('opened_socket =', False)
		users = q.fetch(1000)
		for user in users:
			if ((datetime.datetime.now() - user.creation_date).seconds > 120):
				db.delete(user)
