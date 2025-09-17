from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import User,UserRegistrationSerializer
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role,
            },
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    try: 
        print("====> Request data:", request.data)
        email = request.data.get("email")
        password = request.data.get("password")

        print("=====> email:" , email)
        print("=====> email:" , password)

        user = User.objects.get(email=email)
        
        print("=====> user:" , user)
        if user and not user.is_active:
            return Response({"detail": "Account is not active"}, status=status.HTTP_403_FORBIDDEN)

        if not user or not user.check_password(password):
            return Response({"detail": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token

        return Response(
            {
                "message": "success",
                "data": {
                    "token": str(access_token),
                    "refresh_token": str(refresh),
                },
            }
        )
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def ForgotPassword(request):
    email = request.data.get("email")

    print("=====> email:" , email)

    if not email :
        return Response({"error": "Email requis"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email=email)
        print("=====> user:" , user)
    except User.DoesNotExist:
        return Response({"error": "Aucun utilisateur avec cet email"}, status=status.HTTP_404_NOT_FOUND)
    
    # Génération d'un UID + token 
    uid = urlsafe_base64_encode(force_bytes(user.pk))
  
    token = PasswordResetTokenGenerator().make_token(user) 

    reset_link = f"http://localhost:3000/reset-password/{uid}/{token}/"

    # lien par email 
    print("Lien de réinitialisation :", reset_link)

    return Response({"message": "Email de réinitialisation envoyé", "reset_link": reset_link})

@api_view(['PUT'])
@permission_classes([AllowAny])
def changePassword(request, id):
    password = request.data['password']
    new_password = request.data['new_password']

    obj = get_user_model().objects.get(pk=id)
    if not obj.check_password(raw_password=password):
        return Response({'error': 'password not match'}, status=400)
    else:
        obj.set_password(new_password)
        obj.save()
        return Response({'success': 'password changed successfully'}, status=200)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    try :
        user = request.user
        serializer = UserRegistrationSerializer(user, many=False)
        return Response({
            "message": "User profile retrieved successfully",
            "user": serializer.data
        })
    except Exception as e : 
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUserProfile(request):
    try :
        user = request.user
        serializer = UserRegistrationSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                    {
                        "message": "User profile updated successfully",
                        "user" :  serializer.data
                    }
                )
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


