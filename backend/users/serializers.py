from rest_framework import serializers
from django.contrib.auth import get_user_model
from dj_rest_auth.registration.serializers import RegisterSerializer

User = get_user_model()

class CustomRegisterSerializer(RegisterSerializer):
    """
    Extends the default RegisterSerializer to include additional fields.
    """
    phone_number = serializers.CharField(max_length=15, required=False)
    address = serializers.CharField(required=False)
    city = serializers.CharField(max_length=100, required=False)
    state = serializers.CharField(max_length=100, required=False)
    country = serializers.CharField(max_length=100, required=False)
    postal_code = serializers.CharField(max_length=20, required=False)
    
    def custom_signup(self, request, user):
        user.phone_number = self.validated_data.get('phone_number', '')
        user.address = self.validated_data.get('address', '')
        user.city = self.validated_data.get('city', '')
        user.state = self.validated_data.get('state', '')
        user.country = self.validated_data.get('country', '')
        user.postal_code = self.validated_data.get('postal_code', '')
        user.save()

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    """
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 
                  'phone_number', 'address', 'city', 'state', 'country', 
                  'postal_code', 'profile_picture')
        read_only_fields = ('id', 'email')