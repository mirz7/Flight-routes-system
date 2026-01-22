
from django.db import models
from django.core.validators import MinValueValidator

class Airport(models.Model):
    """
    Model representing an airport with a unique code and position.
    """
    code = models.CharField(max_length=10, unique=True, primary_key=True)
    position = models.IntegerField(
        validators=[MinValueValidator(0)],
        help_text="Position number of the airport"
    )
    
    class Meta:
        ordering = ['code']
    
    def __str__(self):
        return f"Airport {self.code}"


class Route(models.Model):
    """
    Model representing a flight route between airports.
    Routes are directional: from_airport -> to_airport
    """
    DIRECTION_CHOICES = [
        ('left', 'Left'),
        ('right', 'Right'),
    ]
    
    from_airport = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
        related_name='outgoing_routes'
    )
    to_airport = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
        related_name='incoming_routes'
    )
    direction = models.CharField(
        max_length=5,
        choices=DIRECTION_CHOICES
    )
    duration = models.IntegerField(
        validators=[MinValueValidator(1)],
        help_text="Duration in minutes"
    )
    
    class Meta:
        # Ensure no duplicate routes between same airports in same direction
        unique_together = ['from_airport', 'to_airport', 'direction']
        ordering = ['from_airport', 'direction']
    
    def __str__(self):
        return f"{self.from_airport.code} -> {self.to_airport.code} ({self.direction}, {self.duration} min)"