from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
class HomeView(TemplateView):
    template_name = 'website/home.html'


class DocsView(TemplateView):
    template_name = 'website/docs.html'

class AboutUsView(TemplateView):
    template_name = 'website/about-us.html'