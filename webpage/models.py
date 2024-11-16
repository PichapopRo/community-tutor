from django.db import models
from django.contrib.auth.models import User

class Address(models.Model):
    address_id = models.AutoField(primary_key=True)
    street_address = models.CharField(max_length=255)
    sub_district = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    province = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.street_address}, {self.sub_district}, {self.district}, {self.province}, {self.zip_code}"


class UserInfo(models.Model):
    user_id = models.AutoField(primary_key=True)
    phone_number = models.CharField(max_length=20, unique=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user_id} - {self.phone_number}"


class Session(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    course_date_time = models.DateTimeField()
    course_description = models.TextField(null=True, blank=True)  # Making description optional
    start_date = models.DateField()
    end_date = models.DateField()
    location = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.course} - {self.start_date} to {self.end_date}"


class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=255)

    def __str__(self):
        return self.course_name


class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    session_id = models.ForeignKey(Session, on_delete=models.CASCADE)
    learner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='learner_transactions')
    tutor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tutor_transactions')
    date = models.DateField()
    time = models.TimeField()
    duration = models.DurationField()
    fee = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Transaction {self.transaction_id} - {self.learner} and {self.tutor}"


class Enroll(models.Model):
    enroll_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user_id', 'session')

    def __str__(self):
        return f"Enrollment: {self.user_id} in {self.session}"


class Tutor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    teaching_interests = models.ManyToManyField(Course)

    def __str__(self):
        return f"Tutor: {self.user.username}"


class Learner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    learning_interests = models.ManyToManyField(Course)

    def __str__(self):
        return f"Learner: {self.user.username}"
