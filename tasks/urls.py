from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("signup/", views.sigup, name="signup"),
    path("tasks/", views.pending_tasks, name="tasks"),
    path("tasks/completed/", views.completed_tasks, name="completedTasks"),
    path("logout/", views.signout, name="logout"),
    path("signin/", views.signin, name="signin"),
    path("tasks/new/", views.create_task, name="createTask"),
    path("tasks/<int:task_id>/", views.task_detail, name="taskDetail"),
    path("tasks/<int:task_id>/complete/", views.complete_task, name="completeTask"),
    path("tasks/<int:task_id>/delete/", views.delete_task, name="deleteTask"),
    path("tasks/edit/<int:task_id>/", views.edit_task, name="editTask"),
]
