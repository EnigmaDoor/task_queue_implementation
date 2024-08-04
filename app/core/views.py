from django.shortcuts import redirect, render
from django.http import HttpResponse

from .models import Task
from .forms import TasksForm

def index(request):
    return HttpResponse("Hello world!")

def create_task_view(request):
    context = {}
    form = TasksForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('core:show_task_url')
    context['form'] = form
    return render(request, "create_task_view.html", context)

def show_task_view(request):
    context = {}
    tasks = Task.objects.all()
    context['tasks'] = tasks
    return render(request, "show_task_view.html", context)
