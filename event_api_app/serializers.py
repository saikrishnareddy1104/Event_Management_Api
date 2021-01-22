from rest_framework import serializers
from .models import  Events , Participants
from django.contrib.auth.models import User




class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = ['event_id','event_name','event_location','event_type','organiser_email','date','vacancy']




class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participants
        fields = ['participant_id','username','email','events_registerd']  



class SingleEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participants
        fields = ['participant_id','username','email']





# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])

        return user
