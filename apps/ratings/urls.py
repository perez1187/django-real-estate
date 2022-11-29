from django.urls import path

from . import views

urlpatterns = [
    path("<str:profile_id>/", views.create_agent_review, name="create-rating") #in views in def we have profile_id
]