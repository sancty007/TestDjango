from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import User, UserLoginSerializer, UserRegistrationSerializer

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