Creating a FB Messenger Echo Bot with Heroku and Django
=======


I am assuming a beginner level of familiarity with both Heroku and Django.

Requirements:
-------------

 - Virtualenv
 - Postgres
 - Python 2.7
 - pip
 - Facebook Account
 - Facebook Page
 - Heroku Account

Getting Started
---------------

To start out, make sure you have the Heroku Command Line Interface (CLI) Installed.

Heroku CLI can be download and installed [here](https://www.google.com/webhp?sourceid=chrome-instant&ion=1&espv=2&ie=UTF-8#q=heroku%20cli)

Open up a terminal window and login to Heroku with:

    heroku login

Setting up Django
-----------------

Next, you'll want to get your Django project going with the following:

	django-admin startproject fbbot

Now initialize it as a git repo:

    git init
Now create a virtual environment (we're literally calling our environment 'env' here):

    virtualenv env
Awesome now activate your environment with:

    source env/bin/activate
Run the following pip installs for all you'll need:

    pip install Django
    pip install gunicorn
    pip install psycopg2
    pip install requests

Okay now we are rolling, assuming you are still in the fbbot directory we intially made, you need to create a *Procfile* which is required my Heroku:

    sudo nano Procfile
Paste the following in your file:

    web: gunicorn fbbot.wsgi --log-file -
and hit ctrl+X to save.

Now, we've got to make a few changes to our Django project in order to get it running on Heroku. Using your favorite text editor (I use atom) open up your settings.py file:

Edit the `ALLOWED_HOSTS` variable to look like the following:

	ALLOWED_HOSTS = ['*']

 and paste this at the end to ensure static files are collected properly:

	PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
	STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
	STATIC_URL = '/static/'
	STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
	)
Remember that `STATIC_ROOT` is where your static files are collected and `STATICFILES_DIRS` is where your static files live. What the above means is that when Django needs to collect your static files its going to look in the `fbbot/fbbot/static` folder, grab those files and put them in `STATIC_ROOT`.
With that being said, we must manually create a static file in order for Django to know where to look for static files once we push to Heroku (otherwise we may get an error).

Go ahead and make a folder `fbbot/fbbot/static` and save a random txt file in there to ensure it is detected.

Last step before going online, get back in your original project directory and create a requirements file with all your necessary packages (this tells the server what packages need to be installed):

	pip freeze > requirements.txt
You project directory should look as follows at this point:
![](https://cloud.githubusercontent.com/assets/4912421/22401234/d10a2aba-e580-11e6-9396-c42fd83dac10.png)

Now we should be good to go, add and commit everything to your git repo:

	git add .
	git commit -m "initial commit"

Create a Heroku App and push everything:

	Heroku create
	git push heroku master

If everything was set up correctly, your Heroku app url should show the following:

![](https://cloud.githubusercontent.com/assets/4912421/22401886/6837ce48-e599-11e6-960c-66854d28592b.png)


Configuring Your App with Facebook
----------------------------------

Okay now it's time for the fun. Lets head over to the [Facebook developer site](https://developers.facebook.com/), and in the top right corner hit 'Add a New App.'

You should see the following screen,  fill out any display name you'd like and hit 'Apps for Messenger.'

![](https://cloud.githubusercontent.com/assets/4912421/22172296/a3dc7716-df57-11e6-9a6a-18850aebda4e.png)

Next, you should see the following screen. Hit 'Add Product' then 'Messenger' in the sidebar:

![](https://cloud.githubusercontent.com/assets/4912421/22172304/d40cd638-df57-11e6-9c31-f4442507ce5c.png)

 Scroll down to associate your app with your FB Page for token generation, make a note of what your Page Access Token is, as you will need this when trying to send messages from your app.
![](https://cloud.githubusercontent.com/assets/4912421/22172373/995f767e-df59-11e6-9044-35a7fbc684e9.png)

Next you'll want to click '+Add Product' on the left menu and hit 'Webhooks', you'll be presented with options to add a new subscription for a page.

![](https://cloud.githubusercontent.com/assets/4912421/22401728/0ca3ef0e-e593-11e6-8920-e2a5f291b337.png)

You'll want to set up a subscription using the URL for your Heroku app, an arbitrary Verify Token (you can choose), and all messaging options checked.

![](https://cloud.githubusercontent.com/assets/4912421/22401743/a98b3d04-e593-11e6-9cad-60d190bf4f37.png)

You'll notice facebook gives you a callback error if you try to verify and save. That's because we still haven't set up the logic in our Django project to accept the request made by facebook. We'll set this up now and return back later.

Connecting our App to the Web
-----------------------------

Get back in your terminal and make sure that your current directory is your Django project. Start a new app called 'bot':

	python manage.py startapp bot

Head back into your settings.py file and add 'bot' under your INSTALLED_APPS. That array should look like this:

    INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bot',
]

Now you we have to do a couple things:

 1. Set up our **urls.py** files for our whole project and our app (2 different files).
 2. Set up the **views.py** file for our app to match the Verify Token we have set in Facebook.

In your main **urls.py** file (this is for your project not your new 'bot' app), add in a reference to the 'bot' app **urls.py** by editing the urlpatterns list like so:


    urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('bot.urls')),
	]
Now, in the folder for your 'bot' app create a file called **urls.py** and add the following:

	from django.conf.urls import url
	from . import views
	urlpatterns = [
    url(r'^', views.botConnect),
	]
We just created a reference to a view function we have not created, so lets do that now. In your **views.py** file located in the same folder add the following:

	def botConnect(request):
    if request.method == 'GET':
            #Verify Token is based on what you input into Facebook
            if request.GET.get('hub.verify_token') == '123456':
                return HttpResponse(request.GET['hub.challenge'])
            else:
                return HttpResponse('Error')

Note that I am using the verify token I set earlier as '123456' but yours can be different, the only important thing is that these tokens match.

Back in the terminal, lets save all this and push to Heroku:

	git add .
	git commit -m "Enabled Webhook Connection to Facebook"
	git push heroku master

Back in Facebook hit 'Verify and Save' and you should be good to go!

Okay so you're connected. What now?

Setting up your App Logic to Communicate with Facebook
------------------------------------------------------

At this point, we've got to structure our view functions to comply with Facebook's Messengers callback structure. Head over to the [Facebook for Developers Webhook Common Format](https://developers.facebook.com/docs/messenger-platform/webhook-reference#format) section and you'll see that POST requests have the following JSON formatting:

    {
	  "object":"page",
	  "entry":[
	    {
	      "id":"PAGE_ID",
	      "messaging":[
	        {
	          "sender":{
	            "id":"USER_ID"
	          },
	          "recipient":{
	            "id":"PAGE_ID"
	          },
	          "message":{
	          ...
	          "text": "some, text"
	          }
	        }
	      ]
	      "time":1458692752478,
	    }
	  ]
	}

Let's start by setting up our views.py function to receive messages from the messenger which come in as requests.

First, import the json library in your views.py file insert the following at the top:

	import json, requests
	from django.views.decorators.csrf import csrf_exempt
	from django.utils.decorators import method_decorator

A couple notes here:

 - We import json in order to read in the request data in JSON format and turn it into an object (list) that we can manipulate in our code. We also use this when posting the data back to Facebook.
 - We import requests in order to easily post data back to Facebook via the SEND API.
 - We import the method_decorator and csrf_exempt because in Django we always need a csrf_exempt token when posting data.

 Now, lets go in our views.py file and add a couple things. First we need to add a csrf_exempt method decorator to our botConnect method:

	 	@method_decorator(csrf_exempt)
	 	def botConnect(request):
	    if request.method == 'GET':
            #Verify Token is based on what you input into Facebook
            if request.GET.get('hub.verify_token') == '123456':
                return HttpResponse(request.GET['hub.challenge'])
            else:
                return HttpResponse('Error')
Next we need to check if the request being received by our site is a POST request. If it is, we want to define our post URL now, so that we know where our data is going. Remember that page access token we generated earlier? We are going to use that now (this is NOT the verify token you created).

		@method_decorator(csrf_exempt)
		def botConnect(request):
	    if request.method == 'GET':
	            #Verify Token is based on what you input into Facebook
        if request.GET.get('hub.verify_token') == '123456':
            return HttpResponse(request.GET['hub.challenge'])
        else:
            return HttpResponse('Error')
	    if request.method == 'POST':
        postURL = 'https://graph.facebook.com/v2.6/me/messages?access_token=YOURACCESSTOKENHERE'
        return HttpResponse()

Now, we want to use `json.loads()` to actually create an object containing all the data we showed earlier. We want to pass the body of our request to `json.loads()`, however `json.loads()` only accepts unicode strings while `request.body` produces a byte string.  Therefore we will decode request.body and pass it to json.loads to produce a callback object.
This will go under the definition of our postURL variable:

    callback = json.loads(request.body.decode('utf-8'))

The callback object is actually a list of entry objects (shown earlier), so we want to loop through each entry, **then** loop through each `messaging` object to pull pertinent information such as the sender id or message text.

Posting Echo Data to Facebook
-----------------------------

Finally, we want to create a response string that you will post back to Facebook with the information we just pulled. Remember we are posting the information we just extracted from the callback because the intent of our bot is to echo the users input.
The way this will look is as follows:

	        for callbackEntry in callback['entry']:
	            for messagingDict in callbackEntry['messaging']:
	                #Turn the SENDAPI required objects into a string to be posted
	                response = json.dumps({"recipient":{"id":messagingDict['sender']['id']}, "message":{"text":messagingDict['message']['text']}})
	                #post the data back to Facebook
	                requests.post(postURL, headers={"Content-Type": "application/json"},data=response)

Note that here  we are posting data via the `requests` module based on requirements found in  [Facebook Messenger Send API Documentation](https://developers.facebook.com/docs/messenger-platform/send-api-reference), which include:

 1. The url we are posting to
 2. Content type
 3. The actual data we are sending to contain a sender id and a message.

You can read more about the requests module [here](http://docs.python-requests.org/en/master/).

Finally, your **views.py** file should look like this:

	import json, requests
	from pprint import pprint
	from django.shortcuts import render
	from django.http import HttpResponse
	from django.views.decorators.csrf import csrf_exempt
	from django.utils.decorators import method_decorator

	# Create your views here.

	@method_decorator(csrf_exempt)
	def botConnect(request):
	    if request.method == 'GET':
            #Verify Token is based on what you input into Facebook
	        if request.GET.get('hub.verify_token') == '123456':
	            return HttpResponse(request.GET['hub.challenge'])
	        else:
            return HttpResponse('Error')
	    if request.method == 'POST':

	        #Take the callback JSON data and turn it into an object

        callback = json.loads(request.body.decode('utf-8'))

	        #Loop through the callback to pull messaging specific data

	        for callbackEntry in callback['entry']:
	            for messagingDict in callbackEntry['messaging']:

	                response = json.dumps({"recipient":{"id":messagingDict['sender']['id']}, "message":{"text":messagingDict['message']['text']}})


	                requests.post(postURL, headers={"Content-Type": "application/json"},data=response)

        return HttpResponse()

and that should do it! Lets get back in the terminal with our current directory being our project directory, and push changes to our Heroku app.

		git add .
		git commit -m "Added in Echo Functionality"
		git push heroku master

## Results ##

![](https://cloud.githubusercontent.com/assets/4912421/22405962/f00c4db6-e5fe-11e6-9511-2a15efeb207f.png)

For additional details, please refer to the files found in the repository.


## References ##

 1. Facebook Webhook API Reference:
	 https://developers.facebook.com/docs/messenger-platform/webhook-reference

 2.  Facebook Send API Reference:
	https://developers.facebook.com/docs/messenger-platform/send-api-reference
 3. "How to Build a Facebook Messenger Bot Using Django, Ngrok"
 https://abhaykashyap.com/blog/post/tutorial-how-build-facebook-messenger-bot-using-django-ngrok


> Written with [StackEdit](https://stackedit.io/).
