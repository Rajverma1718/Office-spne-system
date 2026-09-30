from django.contrib import admin
from .models import Expense


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = (

        'user',          # ✅ ADD
        'manager',       # ✅ ADD
        'project',
        'amount',
        'final_amount',
        'currency',
        'city',
        'date',
        'status',        # ✅ ADD
    )

    list_filter = (
        'claim_type',
        'travel_type',
        'city',
        'currency',
        'date',
        'status',        # ✅ ADD
        'manager',       # ✅ ADD
    )

    search_fields = (
        'project',
        'city',
        'remarks',
        'user__username',    # ✅ ADD
        'manager__username', # ✅ ADD
    )

    ordering = ('-date',)

    readonly_fields = ('final_amount',)

    fieldsets = (
        ('User Info', {   # ✅ ADD
            'fields': ('user', 'manager', 'status')
        }),

        ('Basic Info', {
            'fields': ('claim_type', 'travel_type', 'city', 'date')
        }),

        ('Expense Details', {
            'fields': ('expense', 'currency', 'conversion_rate')
        }),

        ('Amount Info', {
            'fields': ('amount', 'final_amount')
        }),

        ('Project Info', {
            'fields': ('project',)
        }),

        ('Files', {
            'fields': ('document', 'bill')
        }),

        ('Remarks', {
            'fields': ('remarks',)
        }),
    )