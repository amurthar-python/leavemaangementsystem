from datetime import date

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Model
# from django.core.validators import validate_birthday
# from django.core.validators import validate_number
from django.core.validators import MinValueValidator
from django.core.validators import MaxValueValidator

GENDER_CHOICES = {
    ('M', 'Male'),
    ('F', 'Female'),
}


LEAVETYPE_CHOICES = {
    ('SL', 'Sick Leave'),
    ('CL', 'Casual Leave'),
    ('EL', 'Earned Leave'),
    ('ML', 'Maternity Leave'),
    ('LW', 'Leave Without Pay'),
}

GRADE_CHOICES = {
    (1, 'Grade 1'),
    (2, 'Grade 2'),
    (3, 'Grade 3'),
    (4, 'Grade 4'),
    (5, 'Grade 5'),
}


class Employee(models.Model):
    employee_id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    grade = models.IntegerField(choices=GRADE_CHOICES)
    joining_date = models.DateField(auto_now=True)

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)


class LeaveMaster(models.Model):
    leave_type = models.CharField(max_length=2, choices=LEAVETYPE_CHOICES)
    grade = models.IntegerField(choices=GRADE_CHOICES)
    leave_description = models.CharField(max_length=100)
    number_of_days_in_a_year = models.IntegerField()
    accrual_flag = models.BooleanField(default=False)
    maximum_accrual_days = models.IntegerField(default=0)
    special_leave_flag = models.BooleanField(default=False)


class LeaveRequest(models.Model):
    RequestID = models.IntegerField()
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    request_leave_type = models.ForeignKey(LeaveMaster, on_delete=models.CASCADE, related_name='%(class)s_lt_request')
    request_period_from = models.DateField(auto_now=True)
    request_period_to = models.DateField(auto_now=True)
    approved_period_from = models.DateField(auto_now=True)
    approved_period_to = models.DateField(auto_now=True)
    approved_leave_type = models.ForeignKey(LeaveMaster, on_delete=models.CASCADE, related_name='%(class)s_lt_approve')
    request_comments = models.CharField(max_length=100, blank=True)
    created_user_id = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='%(class)s_requests_created')
    approve_user_id = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='%(class)s_requests_approved')
    approval_flag = models.BooleanField(default=False)
    approved_user_comments = models.CharField(max_length=100, blank=True)

    # def validate_number(self, value):
    #     if self.approval_flag is True and self.maximum_accrual_days < self.number_of_days_in_a_year:
    #         raise ValidationError('%s Accrual days cannot be Less than Number of Days in a Year ' % value)

    # def validate_birthday(self, value):
    #     today = date.today()
    #     born = self.date_of_birth
    #     rest = 1 if (today.month, today.day) < (born.month, born.day) else 0
    #     age = today.year - born.year - rest
    #     if age < 18:
    #         raise ValidationError('%s Date of Birth should be > 18 years ' % value)


class EmployeeLeaveHistory(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    leave_type = models.ForeignKey(LeaveMaster, on_delete=models.PROTECT)
    Calendar_year = models.IntegerField(validators=(MinValueValidator(2012), MaxValueValidator(2035)))
    EligibleDays = models.CharField(max_length=10)
    AvailedDays = models.DecimalField(max_digits=4, decimal_places=1)
    BalanceDays = models.DecimalField(max_digits=4, decimal_places=1)