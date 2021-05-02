from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, TemplateView
from django.contrib.auth.decorators import login_required
from . import scrap_news
from django.http import HttpResponse
from . import mailHandler
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
#recaptcha imports
import json
import urllib
from django.conf import settings
import environ
env = environ.Env()
# reading .env file
environ.Env.read_env()
# Create your views here.


# from . import scrap_news

from . import models
from .models import News

class Homepage(TemplateView):
    template_name= "index.html"

class Shortvisapage(TemplateView):
    template_name= "shortvisa.html"

class Longvisapage(TemplateView):
    template_name= "longvisa.html"

class Studentvisapage(TemplateView):
    template_name= "studentvisa.html"

class workvisapage(TemplateView):
    template_name= "workvisa.html"

class Aboutuspage(TemplateView):
    template_name= "aboutus.html"

class Whyuspage(TemplateView):
    template_name= "whyus.html"

class Comingpage(TemplateView):
    template_name= "coming_soon.html"

class Terms(TemplateView):
    template_name= "terms.html"

class Disclaimer(TemplateView):
    template_name= "disclaimer.html"

class Privacypolicy(TemplateView):
    template_name= "privacy_policy.html"

class Givingitback(TemplateView):
    template_name= "givingItBack.html"

class Contactpage(TemplateView):
    template_name= "contactus.html"
    def get(self, request, *args, **kwargs):
        context={
            'SITE_KEY': env('RECAPTCHA_SITE_KEY')
        }

        return render(request, "contactus.html",context = context)

    def post(self, request, *args, **kwargs):
        data = request.POST
        ''' Begin reCAPTCHA validation '''
        recaptcha_response = request.POST.get('g-recaptcha-response')
        url = 'https://www.google.com/recaptcha/api/siteverify'
        values = {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        data = urllib.parse.urlencode(values).encode()
        req =  urllib.request.Request(url, data=data)
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode())
        ''' End reCAPTCHA validation '''
        if result['success']:
            mailHandler.sendMailToUser(request.POST.get('name'), request.POST.get('email'))
            mailHandler.sendMailToVisaToIreland(request.POST.get('name'), request.POST.get('email'),request.POST.get('phone'),request.POST.get('subject'),request.POST.get('message'))
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('index')
        else:
            messages.info(request, 'Invalid reCAPTCHA. Please try again.')
            context={
            'SITE_KEY': env('RECAPTCHA_SITE_KEY')
            }
            return render(request,"contactus.html",context = context)

class Blog(View):
    def get(self, request, *args, **kwargs):

        render_news = models.News.objects.all()
        context = {
            'news': render_news
        }

        return render(request, 'blogs.html', context=context)

@login_required(login_url='/admin/')
def refresh(request):
    # if(models.News.objects.all().exists()):
    #     for i in range(0, 5):
    #         old_news = models.News.objects.all()[0]
    #         old_news.delete()

    scrapper = scrap_news.Scrapper()

    for i in range(0,5):
        news = models.News.objects.create(
        	title=scrapper.titles[i],
        	date=scrapper.dates[i],
        	description=scrapper.descriptions[i],
        	url=scrapper.urls[i]
            )
        news.save()
        print(scrapper.urls[i])



        new_news = models.News.objects.get(title=scrapper.titles[i])


    return HttpResponse('News fetched successfully!')
