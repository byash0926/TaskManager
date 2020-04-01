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