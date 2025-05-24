from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate

from zoom.models import *
from .forms import *

from django.contrib.auth.decorators import login_required

def hero(request):
    return render(request, 'store/main.html')

@login_required(login_url='login')
def table(request):
    if 'q' in request.GET:
        q = request.GET['q']
        tasks = Task.objects.filter(title__icontains=q)
    else:
        tasks = Task.objects.all()
        
    if not tasks.exists():
        tasks = Task.objects.all()
        
    total_task= tasks.count()
    pending_task = tasks.filter(status=False).count()
    completed_task = tasks.filter(status=True).count()
    
    context = {
        'tasks':tasks,
        'total_task':total_task,
        'pending_task':pending_task,
        'completed_task':completed_task,
    }
    return render(request, 'store/table.html', context)

def create_task(request):
    if not request.user.is_superuser:
        messages.warning(request, "You don't have permissions to create task.")
        return redirect('table')
    
    if request.method == 'POST':
        title = request.POST.get('title')  
        description = request.POST.get('description')
        
        if not title or not description:
            return HttpResponse(
                'Title and description cannot be empty', status=400
            )
        
        Task.objects.create(title=title, description=description)
        
        messages.success(request, "Task created successfully!")
        
        return redirect('table')
    
    return render(request, 'store/create_task.html')

def mark(request, pk):
    task = Task.objects.get(pk=pk)
    task.status = True
    task.save()
    
    messages.success(request, "Task marked successfully!")
    
    return redirect('table')

def unmark(request, pk):
    task = Task.objects.get(pk=pk)
    task.status = False
    
    messages.success(request, "Task un-marked successfully!")

    task.save()
    
    return redirect('table')

def delete(request, pk):
    if not request.user.is_superuser:
        messages.warning(request, "You don't have permissions to delete task.")
        return redirect('table')
    
    task = Task.objects.get(pk=pk)
    task.delete()

    messages.success(request, "Task deleted successfully!")

    return redirect('table')

def update_task(request, pk):
    if not request.user.is_superuser:
        messages.warning(request, "You don't have permissions to update task.")
        return redirect('table')
    
    task = Task.objects.get(pk=pk)
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        
        task.title = title
        task.description = description
        
        task.save()
        
        messages.success(request, "Task updated successfully!")
        
        return redirect('table')
    
    context = {
        'task':task,
    }
    
    return render(request, 'store/update_task.html', context)

def form_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            
            messages.success(request, "Task created successfully!")

            return redirect('table')
    else:
        form = TaskForm
            
    return render(request, 'store/forms.html', {'form':form})

def register_form(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Successfully registered")
            
            return redirect('login')
    
    else:
        form = RegisterForm()
        
    return render(request, 'store/register.html', {'form':form})

def login_form(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, "Successfully Logged in")
                return redirect('table')
    
    else:
        form = LoginForm()
    
    return render(request, 'store/login.html', {'form':form})

def logout_form(request):
    logout(request)
    messages.success(request, 'Successfully Logged Out')
    return redirect('login')



    