from django.urls import path
from .views import People, PeopleDetail
urlpatterns = [
    path('', People.as_view(), name='people'),
    path('<int:pk>', PeopleDetail.as_view())
]