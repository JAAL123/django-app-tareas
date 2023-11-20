from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.core.paginator import Paginator
from .forms import createTaskForm
from .models import Tasks
from django.utils import timezone


# Create your views here.
def sigup(request):
    if request.method == "GET":
        return render(request, "signup.html", {"userForm": UserCreationForm})
    else:
        print(request.POST)
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    username=request.POST["username"],
                    password=request.POST["password1"],
                )
                user.save()
                login(request, user)
                return redirect("tasks")
            except Exception as e:
                print(e)
                return render(
                    request,
                    "sigup.html",
                    {"userForm": UserCreationForm, "error": str(e)},
                )
        return render(
            request,
            "sigup.html",
            {"userForm": UserCreationForm, "error": "Contrasenas no coinciden"},
        )


def signin(request):
    if request.method == "GET":
        return render(request, "signin.html", {"authForm": AuthenticationForm})
    else:
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )
        if user == None:
            return render(
                request,
                "signin.html",
                {
                    "authForm": AuthenticationForm,
                    "error": "Usuario o Contrasena incorrecta",
                },
            )
        else:
            login(request, user)
            return redirect("tasks")


def home(request):
    return render(request, "home.html")


@login_required
def pending_tasks(request):
    tasks = Tasks.objects.filter(
        user=request.user, datecompleted__isnull=True
    ).order_by("-important")
    tasks_obj = tasks.count()
    paginator = Paginator(tasks, 6)  #

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    print(tasks_obj)
    return render(request, "tasks.html", {"tasks": page_obj, "tasks_obj": tasks_obj})


@login_required
def completed_tasks(request):
    tasks = Tasks.objects.filter(
        user=request.user, datecompleted__isnull=False
    ).order_by("datecompleted")
    print(tasks)
    return render(request, "completed_tasks.html", {"tasks": tasks})


@login_required
def create_task(request):
    if request.method == "GET":
        return render(request, "create_task.html", {"form": createTaskForm})
    else:
        try:
            form = createTaskForm(request.POST)
            newTask = form.save(commit=False)
            newTask.user = request.user
            newTask.save()
            return redirect("tasks")
        except Exception as e:
            return render(
                request, "create_task.html", {"form": createTaskForm, "error": str(e)}
            )


@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Tasks, pk=task_id)
    return render(request, "task_detail.html", {"task": task})


@login_required
def edit_task(request, task_id):
    if request.method == "GET":
        task = get_object_or_404(Tasks, pk=task_id, user=request.user)
        form = createTaskForm(instance=task)
        return render(request, "edit_task.html", {"task": task, "form": form})
    else:
        try:
            task = get_object_or_404(Tasks, pk=task_id, user=request.user)
            form = createTaskForm(request.POST, instance=task)
            form.save()
            return redirect("tasks")
        except Exception as e:
            print(str(e))
            task = get_object_or_404(Tasks, pk=task_id, user=request.user)
            form = createTaskForm(request.POST, instance=task)
            return render(
                request, "edit_task.html", {"task": task, "form": form, "error": str(e)}
            )


@login_required
def complete_task(request, task_id):
    if request.method == "POST":
        try:
            task = get_object_or_404(Tasks, pk=task_id, user=request.user)
            task.datecompleted = timezone.now()
            task.save()
            return redirect("tasks")
        except Exception as e:
            print(e)
            return redirect("tasks")


@login_required
def delete_task(request, task_id):
    try:
        task = get_object_or_404(Tasks, pk=task_id, user=request.user)
        task.delete()
        return redirect("tasks")
    except Exception as e:
        print(e)
        return redirect("tasks")


@login_required
def signout(request):
    logout(request)
    return redirect("home")
