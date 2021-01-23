from django.urls import path
from .views import event_list, event_details, single_event, participant_details, participants_list,registration_view
from rest_framework.authtoken.views import obtain_auth_token

# from .views import register

urlpatterns = [
    path('event/',event_list),
    path('event/<pk>',event_details),
    path('user/',participants_list),
    path('user/<pk>',participant_details),
    path('event_user/<pk>',single_event),
    path('register/',registration_view),
    # path('login/',obtain_auth_token)
    
        
]
