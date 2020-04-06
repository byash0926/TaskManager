from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'task'

urlpatterns = [

    path( '' , views.IndexView.as_view() , name='index'),
    path( 'register/' , views.UserFromView.as_view() , name='register'),
    path( 'login/' , views.LoginView.as_view() , name='login'),
    path( 'logout/' , views.logout , name='logout'),
    path( 'task/create', views.TaskCreate.as_view(), name='TaskCreate'),
    path( 'task/<int:pk>', views.TaskUpdate.as_view(), name='TaskUpdate'),
    path( 'task/<int:pk>/delete', views.TaskDelete.as_view(), name='TaskDelete'),


    #rest-API
    path( 'api/login/' , obtain_auth_token , name='api-login'),
    path( 'api/logout/' , views.Logout.as_view() , name='api-logout'),
    path( 'api/register/' , views.registerView , name='api-register'),
    path( 'api/task/' , views.TaskList.as_view() , name='api-index'),
    path( 'api/task/', views.TaskList.as_view(), name='api-TaskCreate'),
    path( 'api/task/<int:pk>', views.TaskUpdate.as_view(), name='api-TaskUpdate'),
    path( 'api/task/<int:pk>/delete', views.TaskDelete.as_view(), name='api-TaskDelete')


    
]
