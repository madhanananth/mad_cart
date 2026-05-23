from rest_framework import viewsets,status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from.models import Address
from .serializers import CustomerProfileSerializer,AddressSerializer,LoginSerializer
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import authenticate



# customer view

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


#Address view set here...

class AddressViewSet(viewsets.ViewSet):

    permission_classes =[IsAuthenticated]

    #list the Address
    @action(detail=False, methods=["get"])
    def list_address(self, request):
         addresses =Address.objects.filter(customer =request.user)
         serializer = AddressSerializer(addresses, many=True)
         return Response(serializer.data, status=status.HTTP_200_OK)
    
    #get the single Address by Id
    @action(detail=True, methods=["get"])
    def retrieve_address(self, request,pk=None):

        try:
            address =Address.objects.get(pk=pk ,customer =request.user)

        except Address.DoesNotExist:
            return Response({'Error' : 'Address not Found'}, status=status.HTTP_404_NOT_FOUND )
        
        serializer = AddressSerializer(address)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # Create Address Endpoint

    @action(detail=False, methods=['post'] )
    def create_address(self, request):

        serializer = AddressSerializer(data=request.data,context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #PUT - Update by id

    @action(detail=True, methods=["put"])
    def update_address(self, request, pk=None):

        try:
            address = Address.objects.get(pk=pk, customer= request.user)

        except Address.DoesNotExist:
            return Response({'Error':'Addreess not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = AddressSerializer(address, data=request.data , context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #   DELETE - addess delete by id

    @action(detail=True, methods=['delete'])
    def delete_address(self,request, pk=None):
        try:
            address = Address.objects.get(pk=pk, customer=request.user)

        except Address.DoesNotExist:
            return Response({'Error': 'Address not Found'}, status=status.HTTP_400_BAD_REQUEST)  
        
        address.delete()
        return Response({'Messages':'Address deleted Successfully..'}, status=status.HTTP_204_NO_CONTENT)

