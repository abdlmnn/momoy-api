from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)  # Dog, Cat, etc.
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"
