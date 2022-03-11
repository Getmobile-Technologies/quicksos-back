import random
import string
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, authentication_classes, permission_classes 
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from accounts.permissions import IsAdmin
from .serializers import ChangePasswordSerializer, LoginSerializer, UserSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth import get_user_model
from .helpers.generators import generate_password


import cloudinary
import cloudinary.uploader



User = get_user_model()


@swagger_auto_schema(methods=['POST'], request_body=UserSerializer())
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdmin])
def add_admin(request):
    

    if request.method == 'POST':
        
        serializer = UserSerializer(data = request.data)
        
        if serializer.is_valid():
            role = serializer.validated_data['role']

            if request.user.is_superuser != True and role=='admin':
                raise PermissionDenied(detail={
                    "message":"You do not have permission to add another admin"
                }) 
            

            
            serializer.validated_data['password'] = generate_password() 
            serializer.save()
            
            data = {
                'message' : "Success",
                'data' : serializer.data,
            }

            return Response(data, status = status.HTTP_201_CREATED)

        else:
            data = {
                
                'message' : "failed",
                'error' : serializer.errors,
            }

            return Response(data, status = status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdminUser])
def get_user(request):
    
    """Allows the admin to see all users  """
    if request.method == 'GET':
        users = User.objects.filter(is_active=True)
    
        
        serializer = UserSerializer(users, many =True)
        data = {
  
                'message' : "success",
                'data' : serializer.data,
            }

        return Response(data, status=status.HTTP_200_OK)
    
    
    
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdmin])
def get_agents(request):
    
    """Allows the admin to see all agents  """
    if request.method == 'GET':
        users = User.objects.filter(is_active=True, role="agent")
    
        
        serializer = UserSerializer(users, many =True)
        data = {
                "message":"success",
                'data' : serializer.data,
            }

        return Response(data, status=status.HTTP_200_OK)
    

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdmin])
def get_escalators(request):
    
    """Allows the admin to see all escalators  """
    if request.method == 'GET':
        users = User.objects.filter(is_active=True, role="escalator")
    
        
        serializer = UserSerializer(users, many =True)
        data = {
                "message":"success",
                'data' : serializer.data,
            }

        return Response(data, status=status.HTTP_200_OK)

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdmin])
def get_escalators(request):
    
    """Allows the admin to see all escalators  """
    if request.method == 'GET':
        users = User.objects.filter(is_active=True, role="first_responder")
    
        
        serializer = UserSerializer(users, many =True)
        data = {
                "message":"success",
                'data' : serializer.data,
            }

        return Response(data, status=status.HTTP_200_OK)


@swagger_auto_schema(methods=['PUT', 'DELETE'], request_body=UserSerializer())
@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def user_detail(request):
    """Allows the logged in user to view their profile, edit or deactivate account. Do not use this view for changing password or resetting password"""
    
    try:
        user = User.objects.get(id = request.user.id, is_active=True)
    
    except User.DoesNotExist:
        data = {
                
                'message' : "Does not exist"
            }

        return Response(data, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        
        data = {
                "message":"success",
                'data' : serializer.data,
            }

        return Response(data, status=status.HTTP_200_OK)

    #Update the profile of the user
    elif request.method == 'PUT':
        serializer = UserSerializer(user, data = request.data, partial=True) 

        if serializer.is_valid():
            
            
            #upload profile picture
            if 'image' in serializer.validated_data.keys():
                try:
                    image = serializer.validated_data.pop('image') #get the image file from the request 
                    img1 = cloudinary.uploader.upload(image, folder = 'quicksos-profile-pics/') #upload the image to cloudinary
                    serializer.validated_data['image_url'] = img1['secure_url'] #save the image url 
                    
                except Exception:
                    data = {
                        
                        'error' : "Unable to upload profile picture"
                    }

                    return Response(data, status = status.HTTP_400_BAD_REQUEST)
            
            serializer.save()

            data = {
                "message":"success",
                'data' : serializer.data,
            }

            return Response(data, status = status.HTTP_201_CREATED)

        else:
            data = {
                
                "message":"failed",
                'error' : serializer.errors,
            }

            return Response(data, status = status.HTTP_400_BAD_REQUEST)

    #delete the account
    elif request.method == 'DELETE':
        user.delete()

        data = {
                'message' : "success"
            }

        return Response(data, status = status.HTTP_204_NO_CONTENT)
    

@api_view(['GET', 'DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdmin])
def get_user_detail(request, user_id):
    """Allows the admin to view user profile or deactivate user's account. """
    try:
        user = User.objects.get(id = user_id, is_active=True)
    
    except User.DoesNotExist:
        data = {
                
                'message' : "Does not exist"
            }

        return Response(data, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        
        data = {
                "message":"success",
                'data' : serializer.data,
            }

        return Response(data, status=status.HTTP_200_OK)

    #delete the account
    elif request.method == 'DELETE':
        user.is_active = False
        user.save()

        data = {
                'message' : "Deleted Successfully"
            }

        return Response(data, status = status.HTTP_204_NO_CONTENT)

        

@swagger_auto_schema(method='post', request_body=LoginSerializer())
@api_view([ 'POST'])
def user_login(request):
    
    """Allows users to log in to the platform. Sends the jwt refresh and access tokens. Check settings for token life time."""
    
    if request.method == "POST":
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            provider = 'email'
            user = authenticate(request, email = data['email'], password = data['password'])
            if user is not None:
                if user.is_active==True:
                    if user.auth_provider == provider:
                        
                        try:
                            
                            refresh = RefreshToken.for_user(user)

                            user_detail = {}
                            user_detail['id']   = user.id
                            user_detail['first_name'] = user.first_name
                            user_detail['last_name'] = user.last_name
                            user_detail['email'] = user.email
                            user_detail['phone'] = user.phone
                            user_detail['role'] = user.role
                            user_detail['is_admin'] = user.is_admin
                            user_detail['image_url'] = user.image_url
                            user_detail['access'] = str(refresh.access_token)
                            user_detail['refresh'] = str(refresh)
                            user_logged_in.send(sender=user.__class__,
                                                request=request, user=user)

                            data = {
        
                            "message":"success",
                            'data' : user_detail,
                            }
                            return Response(data, status=status.HTTP_200_OK)
                        

                        except Exception as e:
                            raise e
                    else:
                        raise AuthenticationFailed(
                        detail='Please continue your login using ' + user.auth_provider)
                else:
                    data = {
                    
                    'error': 'This account has not been activated'
                    }
                return Response(data, status=status.HTTP_403_FORBIDDEN)

            else:
                data = {
                    
                    'error': 'Please provide a valid email and a password'
                    }
                return Response(data, status=status.HTTP_401_UNAUTHORIZED)
        else:
                data = {
                    
                    'error': serializer.errors
                    }
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
            

@swagger_auto_schema(methods=['POST'], request_body=ChangePasswordSerializer())
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])   
def reset_password(request):
    """Allows users to edit password when logged in."""
    user = request.user
    if request.method == 'POST':
        serializer = ChangePasswordSerializer(data = request.data)
        if serializer.is_valid():
            if check_password(serializer.validated_data['old_password'], user.password):
                if serializer.check_pass():
                    user.set_password(serializer.validated_data['new_password'])
                    user.save()
                    
                    data = {
    
                        'message': "Successfully saved password"
                        }
                    return Response(data, status=status.HTTP_202_ACCEPTED) 
                else:
                    
                    data = {
                        
                        'error': "Please enter matching passwords"
                        }
                    return Response(data, status=status.HTTP_400_BAD_REQUEST)   
        
            else:
                
                data = {
                    
                    'error': "Old password incorrect"
                    }
                return Response(data, status=status.HTTP_403_FORBIDDEN)   
        
            
        else:
            
            data = {
                
                'error': serializer.errors
                }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)   
        

