from django.shortcuts import render
from django.views.generic import View, TemplateView
# Create your views here.


class Homepage(TemplateView):
    template_name= "index.html"

class Contactpage(TemplateView):
    template_name= "contactus.html"    
