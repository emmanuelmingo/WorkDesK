from django.db import models

# Create your models here.
class Admin(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(unique=True)
    role = models.CharField(max_length=100, default='admin')

class Technicians(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(unique=True)
    status = models.CharField(default="available")
    contact = models.CharField(default="123-456-7890")
    role = models.CharField(max_length=100, default='technician')

class Todo(models.Model):
    description = models.CharField(max_length=10000)

class Unavailable(models.Model):
    technician_id = models.CharField()
    reason = models.CharField(max_length=1000)

class Task(models.Model):
    task_id = models.CharField(max_length=10, unique=True, primary_key=True, blank= True)
    title = models.CharField(max_length=500)
    description = models.CharField(max_length=10000)
    technician_name = models.CharField(blank=False, default='Nobody')
    created_at = models.DateTimeField( blank=True)
    start_date = models.DateField( null=True, blank=True)
    due_date = models.DateField()
    status = models.CharField(max_length=100, default= 'Not started')
    priority = models.CharField(max_length=100, default='Low')
    file = models.FileField(upload_to='documents/', blank=True)

    def save(self, *args, **kwargs):
        if not self.task_id:
            last_task = Task.objects.order_by('-task_id').first()

            if last_task and last_task.task_id:
                last_number = int(last_task.task_id[2:])
                new_number = last_number + 1
            else:
                new_number = 1
            
            self.task_id = f"TS{new_number:04d}"
        super().save(*args, **kwargs)