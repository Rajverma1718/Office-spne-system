from django.db import models
from django.contrib.auth.models import User   # ✅ ADD

class Expense(models.Model):

    CLAIM_CHOICES = [
        ('Claimable', 'Claimable'),
        ('Non-Claimable', 'Non-Claimable'),
    ]

    TRAVEL_CHOICES = [
        ('Office', 'Office'),
        ('Client Visit', 'Client Visit'),
    ]

    EXPENSE_CHOICES = [
        ('Traveling Expenses', 'Traveling Expenses'),
        ('Food Expense', 'Food Expense'),
        ('Other', 'Other'),
    ]

    PROJECT_CHOICES = [
        ('Full Stack Web Development', 'Full Stack Web Development'),
        ('Other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),     # ✅ FIX (lowercase for logic)
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    # ✅ ADD (Swipe jaisa)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_expenses'
    )

    manager = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='manager_expenses'
    )

    claim_type = models.CharField(max_length=20, choices=CLAIM_CHOICES)
    travel_type = models.CharField(max_length=20, choices=TRAVEL_CHOICES)
    city = models.CharField(max_length=100, default="Mumbai")
    date = models.DateField()

    expense = models.CharField(max_length=100, choices=EXPENSE_CHOICES)
    currency = models.CharField(max_length=10, default="INR")
    conversion_rate = models.FloatField(default=1.0)

    # unit_value = models.FloatField()
    amount = models.FloatField()
    final_amount = models.FloatField()

    project = models.CharField(max_length=100, choices=PROJECT_CHOICES)

    document = models.FileField(upload_to='documents/', null=True, blank=True)
    bill = models.FileField(upload_to='bills/', null=True, blank=True)

    remarks = models.TextField(null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    # ✅ ADD (optional but useful like swipe)
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.project} ({self.status})"