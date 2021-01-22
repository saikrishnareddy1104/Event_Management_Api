from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from . import models    
from .serializers import EventSerializer,ParticipantSerializer,SingleEventSerializer
from rest_framework import generics
from rest_framework import mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

@api_view(['GET','POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def event_list(request):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
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




@api_view(['GET','PUT','DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def event_details(request,pk):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    try:
        Events = models.Events.objects.get(pk=pk)
    except models.Events.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

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
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])

def participants_list(request):
    
    if request.method == 'GET':
        participants = models.Participants.objects.all()
        serializers = ParticipantSerializer(participants,many=True)
        return Response(serializers.data)

    elif(request.method == 'POST'):
        serializers = ParticipantSerializer(data=request.data)
        if serializers.is_valid():
           
            for i in request.data['events_registerd']:
                # print(i)
                # print(models.Events.objects.filter(event_id=i).values('vacancy')[0]['vacancy'])
                a=models.Events.objects.get(event_id=i)
                count=a.vacancy
                count=count-1
                a.vacancy=count
                a.save()
                # models.Events.objects.filter(event_id=i).values('vacancy')[0]['vacancy']=models.Events.objects.filter(event_id=i).values('vacancy')[0]['vacancy']-1
            # print(request.data['events_registersssd'])

            serializers.save()
            return Response(serializers.data,status=status.HTTP_201_CREATED)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET','PUT','DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def participant_details(request,pk):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    try:
        participant = models.Participants.objects.get(participant_id=pk)
    except models.Participants.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializers = ParticipantSerializer(participant)
        return Response(serializers.data)

    elif request.method == 'PUT':
        serializers = ParticipantSerializer(participant,request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        return Response(serializers.errors,status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        participant.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 



@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def single_event(request,pk):
    participant_all = models.Participants.objects.all().filter(events_registerd=pk)
    serializers = SingleEventSerializer(participant_all,many=True)
    return Response(serializers.data)



from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer

# Register API
class register(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })
