from django.urls import  path
from .views import HomeView, DocsView, AboutUsView

app_name = 'website'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('docs/', DocsView.as_view(), name='docs'),
    path('about-us/', AboutUsView.as_view(), name='about-us'),
]