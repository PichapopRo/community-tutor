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
    maximum_participant = models.IntegerField(default=1, null=False)
    participants = models.ManyToManyField(User, related_name='joined_sessions', blank=True)
    fee = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=False)

    def can_apply(self):
        return datetime.now().date() < self.start_date.date()

    def is_full(self):
        return self.participants.count() >= self.maximum_participant

    def get_tutor_info(self):
        return UserInfo.objects.get(user=self.tutor_id)

    def get_pending_transactions(self):
        return self.transaction_set.filter(status='pending')

    def get_applicants(self):
        return User.objects.filter(
            learner_transactions__session_id=self,
            learner_transactions__status='pending')

    def __str__(self):
        return f"{self.category} - {self.start_date} to {self.end_date}"


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=200)

    def __str__(self):
        return self.category_name


class Transaction(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('enrolled', 'Enrolled'),
        ('cancelled', 'Cancelled'),
        ('left', 'Left')
    ]
    transaction_id = models.AutoField(primary_key=True)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    learner = models.ForeignKey(User, on_delete=models.CASCADE,
                                related_name='learner_transactions')
    tutor = models.ForeignKey(User, on_delete=models.CASCADE,
                              related_name='tutor_transactions')
    date = models.DateField()
    time = models.TimeField()
    fee = models.DecimalField(max_digits=10, decimal_places=2,
                              default=0, null=False)
    payment_id = models.CharField(max_length=20, default='')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES,
                              default='pending')

    def __str__(self):
        return (f"Transaction {self.transaction_id} - {self.learner.username} "
                f"with {self.tutor.username}")
