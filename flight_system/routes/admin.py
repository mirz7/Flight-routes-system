# admin.py

from django.contrib import admin
from .models import Airport, Route


@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    """
    Admin interface for Airport model.
    """
    list_display = ['code', 'position']
    search_fields = ['code']
    ordering = ['code']


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    """
    Admin interface for Route model.
    """
    list_display = ['from_airport', 'to_airport', 'direction', 'duration']
    list_filter = ['direction', 'from_airport']
    search_fields = ['from_airport__code', 'to_airport__code']
    ordering = ['from_airport', 'direction']
    
    def get_queryset(self, request):
        """
        Optimize queryset with select_related for foreign keys.
        """
        qs = super().get_queryset(request)
        return qs.select_related('from_airport', 'to_airport')