from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # path('add', views.add_task, name='add_task'),
    # path('edit/<int:pk>', views.edit_task, name='edit_task'),
    # path('delete/<int:pk>', views.delete_task, name='delete_task'),
    # path('task/<int:pk>', views.task_detail, name='task_detail'),
]
