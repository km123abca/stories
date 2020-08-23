

from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
  path('Home/',views.homepage,name='homepage'),
  path('write-story/',views.startStory,name='startStory'),
  path('submit-story/',views.submitStory,name='submitStory'),
  path('imageupload/',views.imageupload,name='imageupload'),
  path('story-list/',views.listOfStories,name='listOfStories'),
  url(r'^login/$', views.LoginFormView.as_view(), name='login'),
  url(r'^register/$', views.UserFormView.as_view(), name='register'),
  url(r'^logout/$', views.logout_user, name='logout_user'),
  url(r'^(?P<storyName>[0-9a-zA-Z\s]+)/(?P<storyAuthor>[0-9a-zA-Z\s]+)/read-story/$', views.readStory,name='readStory'),
]


