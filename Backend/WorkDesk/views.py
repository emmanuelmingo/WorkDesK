from django.shortcuts import render,redirect
from .models import Admin,Technicians,Task,Todo
from django.contrib import messages
from datetime import date,datetime

# Create your views here.
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        role = request.POST.get('role')

        if not email or not password or not role:
            messages.error(request, "All fields are required")
            return redirect('login')
        else:

            if role == 'admin':
                if Admin.objects.filter(email=email).exists():   
                    user = Admin.objects.get(email=email)
                    if password == user.password:
                        request.session['admin_id'] = user.id
                        request.session.set_expiry(1800)
                        return redirect('admin_dashboard')
                    else:
                        messages.error(request, "Invalid credentials")
                        return redirect('login')  
                else:
                    messages.error(request, "User does not exist")
                    return redirect('login')        

            elif role == 'technician':
                if Technicians.objects.filter(email=email).exists():   
                    user = Technicians.objects.get(email=email)
                    if password == user.password:
                        request.session['technician_id'] = user.id
                        request.session.set_expiry(1800)
                        return redirect('technician_dashboard')
                    else:
                        messages.error(request, "Invalid credentials")
                        return redirect('login')  
                else:
                    messages.error(request, "Technician does not exist")
                    return redirect('login')        

            else:
                messages.error(request, "Invalid role selected")
                return redirect('login')  
    else:
        return render(request, 'login.html')

def admin_dashboard(request):
    if 'admin_id' not in request.session:
        messages.info(request, "Session expired. Please log in again.")
        return redirect('login')
    else:
        todo = Todo.objects.all()
        total_tasks = Task.objects.count()
        completed_tasks = Task.objects.filter(status='Completed').count()
        in_progress_tasks = Task.objects.filter(status='In progress').count()
        backlog_tasks = Task.objects.filter(status='Not started').count()
        date_today = date.today()
        time_today = datetime.now().time()
        context={
            'total_tasks':total_tasks,
            'completed_tasks':completed_tasks,
            'in_progress_tasks':in_progress_tasks,
            'backlog_tasks':backlog_tasks,
            'date_today':date_today.strftime("%b %d, %Y"),
            'time_today':time_today.strftime("%H:%M %p"),
            'todo':todo
        }

        return render(request, 'index.html', context)

def technician_dashboard(request):
    if 'technician_id' not in request.session:
        messages.info(request, "Session expired. Please log in again.")
        return redirect('login')
    else:
        technicians = Technicians.objects.filter(id=request.session['technician_id']).get()
        technician_name = Technicians.objects.filter(id=request.session['technician_id']).get().name
        tasks = Task.objects.filter(technician_name=technician_name)
        return render(request, 'tech_dashboard.html',{'technicians':technicians, 'tasks':tasks})

def task(request):
    admin_id = request.session.get('admin_id')
    technicians = Technicians.objects.all()
    tasks = Task.objects.all()
    admin = Admin.objects.filter(id=admin_id).get() 

    if request.method == 'POST':
        technician_name = request.POST.get('technicians')
        priority = request.POST.get('priority')

        request.session['filter_priority'] = priority
        request.session['filter_technician'] = technician_name

        return redirect('task')  

    else:
        
        priority = request.session.get('filter_priority', '')
        technician_name = request.session.get('filter_technician', '')

        if priority:
            tasks = tasks.filter(priority=priority)
        elif technician_name:
            tasks = tasks.filter(technician_name=technician_name)
    
    if 'filter_priority' in request.session:
            del request.session['filter_priority']
    if 'filter_technician' in request.session:
            del request.session['filter_technician']
    return render(request, 'task.html', {
        'technicians': technicians,
        'tasks': tasks,
        'admin': admin
    })

def task_detail(request,pk,role):
    task = Task.objects.filter(task_id = pk).get()
    technician_name = task.technician_name
    technician = Technicians.objects.filter(name=technician_name).get()
    if role == 'technician':
        if request.method == 'POST':
            if task.status == 'Not started':
                Task.objects.filter(task_id = pk).update(status = 'In progress')
                messages.success(request, "Task is now in progress")
                return redirect('technician_dashboard')
            elif task.status == 'In progress':
                file = request.FILES.get('file')
                if file:
                    Task.objects.filter(task_id = pk).update(status = 'Completed', file=file)
                    messages.success(request, "Task marked as completed")
                    return redirect('technician_dashboard')
                else:
                    messages.error(request, "Please upload a file")
                    return redirect('task_detail', pk=pk, role=role)
        return render(request, 'tech_task_detail.html', {'task':task, 'technician':technician})
    else:
        return render(request, 'task_detail.html', {'task':task})

def assign_task(request):
    if request.method == 'POST':
         title = request.POST['title']
         description = request.POST['description']
         technician_name = request.POST.get('technician')
         priority = request.POST.get('priority')
         due_date = request.POST['due_date']
         created_at = date.today()

         date_obj = datetime.strptime(due_date, '%Y-%m-%d').date()

         if not title or not description or not technician_name or not priority or not due_date:
             messages.error(request,'All fields required')
             return redirect('assign_task')
         else:
             if date_obj < date.today():
                 messages.error(request, 'Enter a valid date')
                 return redirect('assign_task')
             else:
                 task = Task.objects.create(
                     title = title,
                     description = description,
                     technician_name = technician_name,
                     priority = priority,
                     due_date = due_date,
                     created_at = created_at
                 )
                 
                 task.save()
                 messages.success(request, "Task successfully registered")
                 return redirect('task')
             
def technicians(request):
    technicians = Technicians.objects.all()
    return render(request, 'technician.html', {'technicians':technicians})
def add_todo(request):
    if request.method == 'POST':
        description = request.POST.get('description')
        if description:
            todo = Todo.objects.create(description=description)
            todo.save()
            messages.success(request, "To-do item added successfully.")
        else:
            messages.error(request, "Description cannot be empty.")
    return redirect('admin_dashboard')