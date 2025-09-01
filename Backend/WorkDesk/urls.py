from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('admin_dashboard', views.admin_dashboard, name='admin_dashboard'),
    path('technician_dashboard', views.technician_dashboard, name='technician_dashboard'),
    path('task', views.task, name='task'),
    path('assign_task', views.assign_task, name='assign_task'),
    path('task/<str:pk>/<str:role>', views.task_detail, name='task_detail'),
    path('task/<str:pk>', views.delete_task, name='delete_task'),
    path('technicians', views.technicians, name='technicians'),
    path('add_todo', views.add_todo, name='add_todo'),
    path('admin_dashboard/<str:pk>', views.delete_todo, name='delete_todo'),
    path('edit_todo/<int:pk>/', views.edit_todo, name='edit_todo'),
]