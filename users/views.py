from rest_framework import viewsets,status
from rest_framework.decorators import action
from rest_framework.response import Response
from.models import Address
from .serializers import CustomerProfileSerializer,AddressSerializer,LoginSerializer
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import authenticate



# Create your views here.

class CustomerProfileViewSet(viewsets.ViewSet):

    @action(detail=False , methods=['post'])
    def register(self, request):

        serializer = CustomerProfileSerializer(data=request.data)

        if serializer.is_valid():
            customer = serializer.save()
            token = AccessToken.for_user(customer)
            return Response({
                'access' : str(token)},
                status = status.HTTP_201_CREATED
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False , methods=['post'])
    def login(self,request):    

        serializer = LoginSerializer(data= request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(email=email, password=password)

            if user:
                token = AccessToken.for_user(user)
                return Response({
                    'access' : str(token)},
                    status = status.HTTP_201_CREATED
                    )
            return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddressViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['post'])
    def add_address(self, request):
        serializer = AddressSerializer(data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

