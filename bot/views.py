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
        postURL = 'https://graph.facebook.com/v2.6/me/messages?access_token=EAAC5ZCJYIGZBkBAGlHTvNAjvSpOcXEcTj9ZCGcecXv9aKniHZC1EAX41EsAXH9ptQK739PyQOel2snJJgGK9w0OKkoeKwOJDyCKviTByAanbzUeqBnlEvEUSpLbxe7VALQ7DHJlSKeFDUn0l8yphjcZCffbqjGMdVsoQcrdGCmgZDZD'
        #Take the callback JSON data and turn it into an object
        callback = json.loads(request.body.decode('utf-8'))
        #Loop through the callback to pull messaging specific data
        for callbackEntry in callback['entry']:
            for messagingDict in callbackEntry['messaging']:
                #Turn the SENDAPI required objects into a string to be posted
                response = json.dumps({"recipient":{"id":messagingDict['sender']['id']}, "message":{"text":messagingDict['message']['text']}})
                #post the data back to Facebook
                requests.post(postURL, headers={"Content-Type": "application/json"},data=response)
        return HttpResponse()
