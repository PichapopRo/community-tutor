from datetime import datetime

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
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, unique=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    date_of_birth = models.DateField(default=datetime.now)

    def __str__(self):
        return f"{self.user_id} - {self.phone_number}"


class Session(models.Model):
    session_name = models.CharField(max_length=100, default="")
    tutor_id = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    session_description = models.TextField(null=True, blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.CharField(max_length=255)

    def can_apply(self):
        return datetime.now().date() < self.start_date.date()

    def __str__(self):
        return f"{self.category} - {self.start_date} to {self.end_date}"


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=200)

    def __str__(self):
        return self.category_name


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
    student_id = models.ForeignKey(User, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('student_id', 'session')

    def __str__(self):
        return f"Enrollment: {self.student_id} in {self.session}"
