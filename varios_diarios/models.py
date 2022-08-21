from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.
class VariosDiarios(models.Model):
    concepto = models.TextField(max_length=30, null=True, blank=True)
    cantidad = models.FloatField(validators=[
        MaxValueValidator(1000000),
        MinValueValidator(-1000000),
    ],
                                 null=True,
                                 blank=True)

    def __str__(self):
        return f"<{self.cantidad} - {self.concepto}"