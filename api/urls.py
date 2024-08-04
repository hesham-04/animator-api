from django.urls import path
from .views import MediaCreateView, MediaListView, MediaDetailView
app_name = 'api'
urlpatterns = [
    path('media/', MediaCreateView.as_view(), name='media-create'),
    path('media/list/', MediaListView.as_view(), name='media-list'),
    path('media/<int:pk>/', MediaDetailView.as_view(), name='media-detail'),
]
