from rest_framework import serializers
from .models import  Events , Participants,Account
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


class RegistrationSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model =Account
        fields=['email','username','password','password2']
        extra_kwargs={
            'password':{'write_only':True}
        }
    def save(self):
        account=Account(email=self.validated_data['email'],username=self.validated_data['username'],)
        password = self.validated_data['password']
        password2=self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({'password':'password must match'})
        account.set_password(password)
        account.save()
        return account


# User Serializer
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('id', 'username', 'email')

# # Register Serializer
# class RegisterSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('id', 'username', 'email', 'password')
#         extra_kwargs = {'password': {'write_only': True}}

#     def create(self, validated_data):
#         user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])

#         return user
