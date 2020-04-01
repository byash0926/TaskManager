from django.urls import path
from . import views

app_name = 'task'

urlpatterns = [

    path( '' , views.IndexView.as_view() , name='index'),
    path( 'register/' , views.UserFromView.as_view() , name='register'),
    path( 'login/' , views.LoginView.as_view() , name='login'),
    path( 'logout/' , views.logout , name='logout'),
    path( 'task/create', views.TaskCreate.as_view(), name='TaskCreate'),
    path( 'task/<int:pk>', views.TaskUpdate.as_view(), name='TaskUpdate'),
    path( 'task/<int:pk>/delete', views.TaskDelete.as_view(), name='TaskDelete')


    
]
