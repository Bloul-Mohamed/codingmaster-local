from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import check_password
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import User
from .serializers import (
    UserSerializer,
    UserCreateSerializer,
    UserUpdateSerializer,
    UserLoginSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint for User operations.

    Provides CRUD operations for user management with proper authentication.
    """
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return UserUpdateSerializer
        return UserSerializer

    def get_permissions(self):
        # Allow anyone to register
        if self.action == 'create' or self.action == 'login':
            return [AllowAny()]
        # Only authenticated users can access other actions
        return [IsAuthenticated()]

    @swagger_auto_schema(
        operation_description="List all users",
        responses={200: UserSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new user account",
        request_body=UserCreateSerializer,
        responses={201: UserSerializer()}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Retrieve user details by ID",
        responses={200: UserSerializer()}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update user details by ID",
        request_body=UserUpdateSerializer,
        responses={200: UserSerializer()}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Partially update user details by ID",
        request_body=UserUpdateSerializer,
        responses={200: UserSerializer()}
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete a user account by ID",
        responses={204: "No content"}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="User login with username and password",
        request_body=UserLoginSerializer,
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'token': openapi.Schema(type=openapi.TYPE_STRING),
                    'user_id': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'username': openapi.Schema(type=openapi.TYPE_STRING),
                }
            ),
            400: "Bad request - invalid credentials"
        }
    )
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        """User login endpoint."""
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return Response(
                    {"error": "Invalid username or password"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Check password
            if check_password(password, user.password):
                # Generate or get token - we'll use a simple approach for now
                token_value = f"token_{user.id}_{hash(user.username)}"

                # Return user info and token
                return Response({
                    'token': token_value,
                    'user_id': user.id,
                    'username': user.username,
                    'department': user.depertment
                })
            else:
                return Response(
                    {"error": "Invalid username or password"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Get users by department",
        manual_parameters=[
            openapi.Parameter('department', openapi.IN_QUERY,
                              description="Department name", type=openapi.TYPE_STRING),
        ],
        responses={200: UserSerializer(many=True)}
    )
    @action(detail=False, methods=['get'])
    def by_department(self, request):
        """Filter users by department."""
        department = request.query_params.get('department')
        if not department:
            return Response(
                {"error": "Department parameter is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        users = User.objects.filter(depertment__icontains=department)
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    API endpoint for retrieving and updating the current user's profile.
    """
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Get the current user based on authentication
        # In a real app with proper auth, you'd use request.user
        # For demo, we're assuming the user ID is passed in the request
        user_id = self.request.query_params.get('user_id')
        if not user_id:
            return Response(
                {"error": "User ID is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )
