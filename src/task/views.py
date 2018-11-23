import tweepy
from django.http import *
from django.shortcuts import render_to_response
from django.urls import reverse
from django.contrib.auth import logout
from task.utils import *
from django.views import View
from django.contrib.auth.views import LoginView , LogoutView 
from django.views.generic import ListView

class Main(View):
    def get(self,request):
        if Check().get(request):
            return HttpResponseRedirect(reverse('tweets'))
        else:
            return render_to_response('twitter/login.html')

class MyLogoutView(LogoutView):
    pass


class CallBack(View):
    def get(self,request):
        verifier = request.GET.get('oauth_verifier')
        oauth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        token = request.session.get('request_token')
        request.session.delete('request_token')
        oauth.request_token = token
        oauth.get_access_token(verifier)
        request.session['access_key_tw'] = oauth.access_token
        request.session['access_secret_tw'] = oauth.access_token_secret
        return HttpResponseRedirect(reverse('tweets'))
    
class TweetsView(ListView):
    def get(self,request):
    	if Check().get(request):
    		search = self.request.GET.get('search')
    		api = get_api(request)
    		public_tweets = api.user_timeline(screen_name=request.user.username, count=30)
    		if search:
    			public_tweets =[status for status in tweepy.Cursor(api.search,q=search).items(30)]
    	
    		context = {
    		'public_tweets' : public_tweets
    		}    
    		return render_to_response('twitter/tweets.html', context)
    	else:
    		return HttpResponseRedirect(reverse('main'))

class MyLoginView(View):
    def get(self,request):
        oauth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth_url = oauth.get_authorization_url(True)
        response = HttpResponseRedirect(auth_url)
        request.session['request_token'] = oauth.request_token
        return response


class Check(View):
    def get(self,request):
        try:
            access_key = request.session.get('access_key_tw', None)
            if not access_key:
                return False
        except KeyError:
            return False
        return True
