from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, TemplateView
from django.contrib.auth.decorators import login_required
from . import scrap_news
from django.http import HttpResponse
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

class Aboutuspage(TemplateView):
    template_name= "aboutus.html"

class Whyuspage(TemplateView):
    template_name= "whyus.html"


class Contactpage(TemplateView):
    template_name= "contactus.html"
    def post(self, request):

        form = request.POST
        name = form.get('name')
        email = form.get('email')
        phone = form.get('phone')
        subject = form.get('subject')
        message = form.get('message')

        new_contact = models.Contact.objects.create(
            name=name,
            email=email,
            phone=phone,
            subject=subject,
            message=message

        )
        new_contact.save()
        mailHandler.sendMailToUser(name, email)
        mailHandler.sendMailToVisaToCanada(name, email, phone, subject, message)
        messages.success(request, "Your query has been successfully submitted. We will get back to you soon.")
        return redirect("contactus")

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
