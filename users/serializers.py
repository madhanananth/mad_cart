from rest_framework import serializers
from .models import CustomerProfile,Address



class CustomerProfileSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)

    class Meta:
        model = CustomerProfile
        fields = ['email','password']

    def create(self, validated_data):
        customer = CustomerProfile(email=validated_data['email'])
        customer.set_password(validated_data['password'])
        customer.save()

        return customer

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


    
class AddressSerializer(serializers.ModelSerializer):
    customer = CustomerProfileSerializer(read_only=True) 

    class Meta:
        model = Address
        fields = ['id', 'address_type','customer', 'phone_number','address', 'city', 'postal_code', 'state', 'county']

    def create(self, validated_data):
        request = self.context.get('request')
        customer = request.user
        return Address.objects.create(customer=customer, **validated_data)


