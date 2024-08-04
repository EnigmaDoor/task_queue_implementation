from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.index, name="index"),
    path('create/', views.create_task_view, name='create_task_url'),
    path('show/', views.show_task_view, name='show_task_url'),
]
