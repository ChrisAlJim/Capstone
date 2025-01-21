from django.urls import path
from . import views

urlpatterns = [
    path("ideas/", views.IdeaListCreate.as_view(), name="idea-list"),
    path("ideas/delete/<int:pk>/", views.IdeaDelete.as_view(), name="delete-idea"),
]