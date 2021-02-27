from django.shortcuts import render
from django.views.generic import View, TemplateView
# Create your views here.


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
