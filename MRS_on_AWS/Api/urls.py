from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('thriller.html', views.thrillers, name='thrillers'),
    path('comedy.html', views.comedy, name='comedy'),
    path('drama.html', views.drama, name='drama'),
    path('animated.html', views.animated, name='animated'),
    path('romance.html', views.romance, name='romance'),
    path('action.html', views.action, name='action'),
    path('horror.html', views.horror, name='horror'),
]

