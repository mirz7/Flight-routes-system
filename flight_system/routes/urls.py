# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add-route/', views.add_route, name='add_route'),
    path('find-nth-node/', views.find_nth_node, name='find_nth_node'),
    path('find-longest-route/', views.find_longest_route, name='find_longest_route'),
    path('find-shortest-route/', views.find_shortest_route_between, name='find_shortest_route'),
]