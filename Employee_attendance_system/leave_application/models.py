from django.db import models
from django.contrib.auth.models import User

class LeaveApplication(models.Model):
    LEAVE_TYPES = [
        ('PL', 'Privilege Leave'),
        ('CL', 'Casual Leave'),
        ('SL', 'Sick Leave'),
    ]
    DAY_TYPE = [('Full', 'Full'), ('Half', 'Half')]
    HALF_TYPE = [('First', 'First Half'), ('Second', 'Second Half')]
    STATUS = [('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    period = models.CharField(max_length=100)
    from_date = models.DateField()
    to_date = models.DateField()
    start_day = models.CharField(max_length=10, choices=DAY_TYPE)
    end_day = models.CharField(max_length=10, choices=DAY_TYPE)
    half_start = models.CharField(max_length=10, choices=HALF_TYPE, blank=False, null=False)
    half_end = models.CharField(max_length=10, choices=HALF_TYPE, blank=False, null=False)
    leave_type = models.CharField(max_length=5, choices=LEAVE_TYPES)
    total_days = models.FloatField()
    reason = models.TextField()
    document = models.FileField(upload_to='leave_docs/', blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS, default='pending')
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.leave_type} ({self.from_date} to {self.to_date})"
