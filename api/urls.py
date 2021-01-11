from django.urls import path
from . import views

urlpatterns = [
    path('todos/', views.PendingTodosViewer.as_view()),
    path('todos/completed/', views.CompletedTodosViewer.as_view()),
    path('todos/<int:pk>/', views.SingleTodoViewer.as_view()),
    path('todos/<int:pk>/complete/', views.CompleteTodoViewer.as_view()),
    path('todos/<int:pk>/uncomplete/', views.UncompleteTodoViewer.as_view()),
]