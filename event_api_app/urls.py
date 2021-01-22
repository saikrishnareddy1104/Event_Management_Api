from django.urls import path
from .views import event_list, event_details, single_event, participant_details, participants_list
from .views import register

urlpatterns = [
    path('event/',event_list),
    path('event/<pk>',event_details),
    path('user/',participants_list),
    path('user/<pk>',participant_details),
    path('event_users/<pk>',single_event),
    path('api/register/', register.as_view(), name='register'),  
        
]
