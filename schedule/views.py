from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.db.models import Q
from datetime import datetime
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Stadium, Department, Schedule, checks
from .serializers import (
    StadiumSerializer,
    DepartmentSerializer,
    ScheduleSerializer,
    ChecksSerializer
)


class StadiumViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Stadium operations.

    Provides CRUD operations for stadium management.
    """
    queryset = Stadium.objects.all()
    serializer_class = StadiumSerializer

    @swagger_auto_schema(
        operation_description="List all stadiums or create a new stadium",
        responses={200: StadiumSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Retrieve a specific stadium by ID",
        responses={200: StadiumSerializer()}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new stadium",
        request_body=StadiumSerializer,
        responses={201: StadiumSerializer()}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update a stadium by ID",
        request_body=StadiumSerializer,
        responses={200: StadiumSerializer()}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Partially update a stadium by ID",
        request_body=StadiumSerializer,
        responses={200: StadiumSerializer()}
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete a stadium by ID",
        responses={204: "No content"}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class DepartmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Department operations.

    Provides CRUD operations for department management.
    """
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    @swagger_auto_schema(
        operation_description="List all departments or create a new department",
        responses={200: DepartmentSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Retrieve a specific department by ID",
        responses={200: DepartmentSerializer()}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new department",
        request_body=DepartmentSerializer,
        responses={201: DepartmentSerializer()}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class ScheduleViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Schedule operations.

    Provides CRUD operations for schedule management and additional filtering capabilities.
    """
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer

    @swagger_auto_schema(
        operation_description="List all schedules with optional filtering by date, department, or stadium",
        manual_parameters=[
            openapi.Parameter('date', openapi.IN_QUERY,
                              description="Filter by date (YYYY-MM-DD)", type=openapi.TYPE_STRING),
            openapi.Parameter('department', openapi.IN_QUERY,
                              description="Filter by department ID", type=openapi.TYPE_INTEGER),
            openapi.Parameter('stadium', openapi.IN_QUERY,
                              description="Filter by stadium ID", type=openapi.TYPE_INTEGER),
        ],
        responses={200: ScheduleSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        queryset = self.queryset

        # Filter by date
        date_param = request.query_params.get('date')
        if date_param:
            try:
                date_obj = datetime.strptime(date_param, '%Y-%m-%d').date()
                queryset = queryset.filter(date=date_obj)
            except ValueError:
                return Response(
                    {"error": "Invalid date format. Use YYYY-MM-DD."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Filter by department
        department_param = request.query_params.get('department')
        if department_param:
            queryset = queryset.filter(department_id=department_param)

        # Filter by stadium
        stadium_param = request.query_params.get('stadium')
        if stadium_param:
            queryset = queryset.filter(stadium_id=stadium_param)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Create a new schedule with time conflict validation",
        request_body=ScheduleSerializer,
        responses={
            201: ScheduleSerializer(),
            400: "Bad request - time conflict or invalid data"
        }
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Check for scheduling conflicts
        new_date = serializer.validated_data['date']
        new_start_time = serializer.validated_data['start_time']
        new_end_time = serializer.validated_data['end_time']
        stadium_id = serializer.validated_data['stadium'].id

        # Get all schedules for the same date and stadium
        conflicting_schedules = Schedule.objects.filter(
            date=new_date,
            stadium_id=stadium_id,
            is_active=True
        )

        # Check for time conflicts
        for schedule in conflicting_schedules:
            if (new_start_time < schedule.end_time and
                    new_end_time > schedule.start_time):
                return Response(
                    {"error": "Time conflict with an existing schedule."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Save the schedule if no conflicts
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    @swagger_auto_schema(
        operation_description="Get available time slots for a specific date and stadium",
        manual_parameters=[
            openapi.Parameter('date', openapi.IN_QUERY, description="Date to check (YYYY-MM-DD)",
                              type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('stadium', openapi.IN_QUERY, description="Stadium ID",
                              type=openapi.TYPE_INTEGER, required=True),
        ],
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'start_time': openapi.Schema(type=openapi.TYPE_STRING, format='time'),
                        'end_time': openapi.Schema(type=openapi.TYPE_STRING, format='time'),
                    }
                )
            ),
            400: "Bad request - missing or invalid parameters"
        }
    )
    @action(detail=False, methods=['get'])
    def available_slots(self, request):
        """Get available time slots for a specific date and stadium."""
        date_param = request.query_params.get('date')
        stadium_param = request.query_params.get('stadium')

        if not date_param or not stadium_param:
            return Response(
                {"error": "Both date and stadium parameters are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            date_obj = datetime.strptime(date_param, '%Y-%m-%d').date()
        except ValueError:
            return Response(
                {"error": "Invalid date format. Use YYYY-MM-DD."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get all schedules for the given date and stadium
        schedules = Schedule.objects.filter(
            date=date_obj,
            stadium_id=stadium_param,
            is_active=True
        ).order_by('start_time')

        # Default operating hours (8 AM to 10 PM)
        operating_start = datetime.strptime('08:00', '%H:%M').time()
        operating_end = datetime.strptime('22:00', '%H:%M').time()

        available_slots = []
        current_time = operating_start

        # Find available slots between scheduled times
        for schedule in schedules:
            if current_time < schedule.start_time:
                available_slots.append({
                    'start_time': current_time.strftime('%H:%M'),
                    'end_time': schedule.start_time.strftime('%H:%M')
                })
            current_time = schedule.end_time

        # Add final slot if there's time left after the last schedule
        if schedules and current_time < operating_end:
            available_slots.append({
                'start_time': current_time.strftime('%H:%M'),
                'end_time': operating_end.strftime('%H:%M')
            })

        # If no schedules for the day, the entire day is available
        if not schedules:
            available_slots.append({
                'start_time': operating_start.strftime('%H:%M'),
                'end_time': operating_end.strftime('%H:%M')
            })

        return Response(available_slots)


class ChecksViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Checks operations.

    Provides CRUD operations for usage tracking.
    """
    queryset = checks.objects.all()
    serializer_class = ChecksSerializer

    @swagger_auto_schema(
        operation_description="Increment counter for a department-stadium pair",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['department', 'stadium'],
            properties={
                'department': openapi.Schema(type=openapi.TYPE_INTEGER),
                'stadium': openapi.Schema(type=openapi.TYPE_INTEGER),
            }
        ),
        responses={
            200: ChecksSerializer(),
            400: "Bad request - missing or invalid parameters"
        }
    )
    @action(detail=False, methods=['post'])
    def increment_counter(self, request):
        """Increment counter for department usage of a stadium."""
        department_id = request.data.get('department')
        stadium_id = request.data.get('stadium')

        if not department_id or not stadium_id:
            return Response(
                {"error": "Both department and stadium IDs are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get or create check record
        check_obj, created = checks.objects.get_or_create(
            depertment_id=department_id,
            stadium_id=stadium_id,
            defaults={'counter': 0}
        )

        # Increment counter
        check_obj.counter += 1
        check_obj.save()

        serializer = self.get_serializer(check_obj)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Get usage statistics by stadium or department",
        manual_parameters=[
            openapi.Parameter('department', openapi.IN_QUERY,
                              description="Filter by department ID", type=openapi.TYPE_INTEGER),
            openapi.Parameter('stadium', openapi.IN_QUERY,
                              description="Filter by stadium ID", type=openapi.TYPE_INTEGER),
        ],
        responses={200: ChecksSerializer(many=True)}
    )
    @action(detail=False, methods=['get'])
    def usage_stats(self, request):
        """Get usage statistics filtered by stadium or department."""
        queryset = self.queryset

        department_param = request.query_params.get('department')
        stadium_param = request.query_params.get('stadium')

        if department_param:
            queryset = queryset.filter(depertment_id=department_param)

        if stadium_param:
            queryset = queryset.filter(stadium_id=stadium_param)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
