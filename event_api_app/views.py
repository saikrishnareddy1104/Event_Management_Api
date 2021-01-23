from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from . import models    
from .serializers import EventSerializer,ParticipantSerializer,SingleEventSerializer,RegistrationSerializer
from rest_framework import generics
from rest_framework import mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.db.models.signals import post_save

from rest_framework.authtoken.models import Token

# Create your views here.
  
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def event_list(request):
    
    if request.method == 'GET':
        return get_request(request)

    elif(request.method == 'POST'):
        return post_request(request)
       

def post_request(request):
    serializers = EventSerializer(data=request.data)
    if serializers.is_valid():
        serializers.save()
        return Response(serializers.data,status=status.HTTP_201_CREATED)
    return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)

def get_request(request):
    Events = models.Events.objects.all()
    serializers = EventSerializer(Events,many=True)
    return Response(serializers.data)


#############################################################

@api_view(['GET','PUT','DELETE'])
@permission_classes([IsAuthenticated])
def event_details(request,pk):

    try:
        Events = models.Events.objects.get(pk=pk)
    except models.Events.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user=request.user
    if Events.organiser_email != user:
        return Response({'response':'you dont have permission to view/edit'})  
    
    if request.method == 'GET':
       return get_request_event_details(request,Events)

    elif request.method == 'PUT':
        return put_request_event_details(request,Events)
        

    elif request.method == 'DELETE':
        return delete_request_event_details(request,Events)




def  get_request_event_details(request,Events):  
    serializers = EventSerializer(Events)
    return Response(serializers.data)  

def  put_request_event_details(request,Events):  
    serializers = EventSerializer(Events,request.data)
    if serializers.is_valid():
        serializers.save()
        return Response(serializers.data)
    return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)

def  delete_request_event_details(request,Events):  
    Events.delete()
    return Response(status=status.HTTP_204_NO_CONTENT) 

  
#############################################################################


@api_view(['GET','POST'])   
@permission_classes([IsAuthenticated])

def participants_list(request):
    
    if request.method == 'GET':
        return get_participants_list(request)
        
    elif(request.method == 'POST'):
        return post_participants_list(request)
        

def get_participants_list(request):
    participants = models.Participants.objects.all()
    serializers = ParticipantSerializer(participants,many=True)
    return Response(serializers.data)


def post_participants_list(request):
    serializers = ParticipantSerializer(data=request.data)

    if serializers.is_valid():
        for i in request.data['events_registerd']:  
            a=models.Events.objects.get(event_id=i)
            count=a.vacancy
            if count>0:
                count=count-1
                a.vacancy=count
                a.save()
            else:
                return Response({"error": "Event capacity is full"}, status=status.HTTP_204_NO_CONTENT)
            

        serializers.save()
        return Response(serializers.data,status=status.HTTP_201_CREATED)
    return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)

    
########################################################################

@api_view(['GET','PUT','DELETE'])
@permission_classes([IsAuthenticated])
def participant_details(request,pk):
    try:
        participant = models.Participants.objects.get(participant_id=pk)
    except models.Participants.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if participant.email != str(request.user):
        return Response({'response':'you dont have permission to view/edit'}) 
    
    if request.method == 'GET':
        return get_request_participant_details(request,participant)

    elif request.method == 'PUT':
        return put_request_participant_details(request,participant)

    elif request.method == 'DELETE':
         return delete_request_participant_details(request,participant)



def get_request_participant_details(request,participant):
    serializers = ParticipantSerializer(participant)
    return Response(serializers.data)

def put_request_participant_details(request,participant):
    serializers = ParticipantSerializer(participant,request.data)
    if serializers.is_valid():
        serializers.save()
        return Response(serializers.data)
    return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)


def delete_request_participant_details(request,participant):
    event=participant.events_registerd.values_list('pk', flat=True)
    for i in event.iterator():
        a=models.Events.objects.get(event_id=i)
        count=a.vacancy
        count=count+1
        a.vacancy=count
        a.save()
    participant.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)



######################################################################################
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def single_event(request,pk):
    participant_all = models.Participants.objects.all().filter(events_registerd=pk)
    serializers = SingleEventSerializer(participant_all,many=True)
    return Response(serializers.data)


@api_view(['POST',])
def registration_view(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data={}
        if serializer.is_valid():
            account = serializer.save() 
            data['response']="succesfully registered new user"
            data['email']=account.email
            data['username']=account.username
            token = Token.objects.get(user=account).key
            data['token']=token
        else:
            data=serializer.errors
        return Response(data)        





























