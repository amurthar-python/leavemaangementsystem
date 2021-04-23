from django.urls import include, path

from . import views


urlpatterns = [
    path('display', views.display, name='display'),
    path('Leave/<int:empid>', views.leave, name='leave'),
    path('add_employee', views.add_employee, name='add-employee'),
    path('display_employee/<int:empid>', views.display_employee, name='display-employee'),
]