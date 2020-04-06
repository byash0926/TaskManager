from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import View
from django.urls import reverse_lazy
from .models import Task
from .templates.task.forms import UserForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .serializers import TaskSerializer, RegisterSerializer
from rest_framework import generics as rest_generics
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status

# Create your views here.

class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'task/index.html'
    context_object_name = 'all_tasks'
    login_url = '/login/'

    def get_queryset(self):
        return Task.objects.filter(super_task = None, user = self.request.user)

# def index(request):
#     allTask = Task.objects.filter(super_task = None)
#     data = {
#         'all_tasks' : allTask,
#     }
#     return render(request, 'task/index.html', data)

class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['name', 'description']
    login_url = '/login/'

    def form_valid(self, form):
        object = form.save(commit=False)
        object.user = self.request.user
        return super(TaskCreate, self).form_valid(form)

class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['name', 'description']
    login_url = '/login/'

    def get_queryset(self):
        return Task.objects.filter(pk = self.kwargs['pk'], user = self.request.user)


class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('task:index')
    login_url = '/login/'

    def get_queryset(self):
        return Task.objects.filter(pk = self.kwargs['pk'], user = self.request.user)

class UserFromView(View):
    form_class = UserForm
    template_name = 'task/register_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form':form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit = False)

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user.set_password(password)
            user.save()

            user = authenticate(username = username, password = password)

            if user is not None:
                if user.is_active:

                    auth_login(request,user)
                    return redirect('task:index')
        return render(request, self.template_name, {'form':form})


class LoginView(View):
    template_name = 'task/login.html'

    def get(self, request):
        return render(request, self.template_name, {})

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password = password)

        if user is not None:
            if user.is_active:
                auth_login(request,user)
                return redirect('task:index')

        return render(request, self.template_name)


def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
    return redirect('task:login')




class TaskList(rest_generics.ListCreateAPIView):
    
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(super_task = None, user = self.request.user)
    serializer_class = TaskSerializer



class TaskDetail(APIView):
    
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    

    def get_object(self, pk):
        try:
            return Task.objects.filter(pk = pk, user = self.request.user)
        except Tas.DoesNotExist:
            raise Http404
    
    #Retrieve
    def get(self, request, pk, format=None):
        task = self.get_object(pk)
        serializer = TaskSerializer(task)
        return Response(serializer.data)
    
    #update
    def put(self, request, pk, format=None):
        task = self.get_object(pk)
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #delete
    def delete(self, request, pk, format=None):
        task = self.get_object(pk)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def registerView(request):

    if request.method == 'POST':
        serializer = RegisterSerializer(data=request.data)
        data={}

        if serializer.is_valid():
            user = serializer.save()
            data['response'] = 'successfully registered a new user'
            token = Token.objects.create(user=user)
            data['token'] = token.key
        else:
            data=serializer.errors
        return Response(data)

class Logout(APIView):
    def get(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)