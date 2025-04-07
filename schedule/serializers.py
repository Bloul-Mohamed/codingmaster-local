from rest_framework import serializers
from .models import Stadium, Department, Schedule, checks


class StadiumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stadium
        fields = ['id', 'name', 'location', 'capacity', 'is_active', 'image']


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'image_team']


class ScheduleSerializer(serializers.ModelSerializer):
    department_name = serializers.ReadOnlyField(source='department.name')
    stadium_name = serializers.ReadOnlyField(source='stadium.name')

    class Meta:
        model = Schedule
        fields = ['id', 'department', 'department_name', 'date', 'start_time',
                  'end_time', 'is_active', 'stadium', 'stadium_name']


class ChecksSerializer(serializers.ModelSerializer):
    department_name = serializers.ReadOnlyField(source='depertment.name')
    stadium_name = serializers.ReadOnlyField(source='stadium.name')

    class Meta:
        model = checks
        fields = ['id', 'counter', 'depertment',
                  'department_name', 'stadium', 'stadium_name']
