#
#  util -> req.py
#  pyblox
#
#  By Sanjay-B(Sanjay Bhadra)
#  Copyright © 2019- Sanjay-B(Sanjay Bhadra). All rights reserved.
#

import asyncio
import requests_async as requests
import json
import browser_cookie3
# from .strings import Strings

try:
	cookies = list(browser_cookie3.chrome())
except browser_cookie3.BrowserCookieError:
	print('Unable to get cookies.')

class Req:

	async def getAllCookies():
		#return cookies
		session = requests.Session()
		response = await session.get("https://www.roblox.com/home")
		print(session.cookies.get_dict())


	'''
	@method 
		request(t=String,url=String,*args,**kwargs)

	@params 
		t = Type of Request(GET or POST)
		url = URL

	@optionals 

		payload = Dictionary Payload
		header = Request Headers
		cookies = cookie

	@result 
		Returns request response wholesale as a tuple

	@example 1:

		# GET Request
		response = Req.request(t="GET",url="http://httpbin.org/get")

		# You can get the status of the request by doing:
		response[0]

		# And so on... its a tuple so this also works as a shorthand:
		response = Req.request(t="GET",url="http://httpbin.org/get")[0]


	@example 2:

		# POST Request
		data = {"Username":"JohnDoe","Password":"JaneDoe"}

		# Data you want to send as a payload
		response = Req.request(t="POST",url="http//httpbin.org/post",payload=data)

		# Again, all data is returned wholesale as a tuple so this works:
		response[0] # Gets you the status of the request

		# Once again, this works as a shorthand:
		response = Req.request(t="POST",url"http://httpbin.org/post",payload=data)[0]
	'''

	async def request(t=str,url=str,*args,**kwargs):
		payload = kwargs.get('payload',None)
		header = kwargs.get('header',{})
		cookies = kwargs.get('cookies',None)

		if t == "GET" or "POST" or "PATCH" or "DEL":
			method = t.replace('DEL', 'delete')
			request = await requests.request(method, str(url), data=payload or None, headers=header, cookies=cookies or {})
			statusCode = request.status_code
			content = request.content
			headers = request.headers
			encoding = request.encoding
			json = request.json()

			# resend request with xcsrf token
			if statusCode == 403 and 'X-CSRF-TOKEN' in headers:
				kwargs['headers']['X-CSRF-TOKEN'] = headers['X-CSRF-TOKEN']
				return request(t=t, url=url, *args, **kwargs)

			# if there is no xcsrf token in reponse headers or it is not required then return the response
			return statusCode, content, headers, encoding, json


		elif t == 'BLANK_POST':
			request = await requests.post(str(url),headers=header)
			statusCode = request.status_code
			content = request.content
			headers = request.headers
			encoding = request.encoding
			json = request.json()
			return statusCode,content,headers,encoding,json

		elif t == "DOUBLE_POST":
			pass

