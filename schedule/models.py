from django.db import models

# Create your models here.


class Stadium(models.Model):

    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    capacity = models.IntegerField()
    is_active = models.BooleanField(default=True)
    image = models.ImageField(
        upload_to='stadium_images/', blank=True, null=True)


class Department(models.Model):
    name = models.CharField(max_length=100)
    image_team = models.ImageField(
        upload_to='team_images/', blank=True, null=True)

    def __str__(self):
        return self.name


class Schedule(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_active = models.BooleanField(default=True)
    stadium = models.ForeignKey(Stadium, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.department.name} - {self.date} {self.start_time}-{self.end_time}"


class checks(models.Model):
    counter = models.IntegerField(default=0)
    depertment = models.ForeignKey(Department, on_delete=models.CASCADE)
    stadium = models.ForeignKey(Stadium, on_delete=models.CASCADE)
