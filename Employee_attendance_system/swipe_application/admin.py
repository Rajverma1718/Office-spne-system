from django.contrib import admin
from .models import SwipeApplication

class SwipeApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'in_time', 'out_time', 'status', 'applied_at')
    list_filter = ('user', 'applied_at')
    search_fields = ('user__username', 'status')

admin.site.register(SwipeApplication, SwipeApplicationAdmin)
