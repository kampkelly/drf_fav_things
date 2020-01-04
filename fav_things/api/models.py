from django.db import models
from django_mysql.models import JSONField

# Create your models here.

class CommonFieldsMixin(models.Model):
    """Add created_at and updated_at fields."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        """Define metadata options."""

        abstract = True


class Category(CommonFieldsMixin):
    name = models.CharField(max_length=250,null=False,unique=True)

    def __str__(self):
        """A string representation of the model."""
        return self.name


class Audit(CommonFieldsMixin):
    log = models.CharField(max_length=255,null=False)


class FavoriteThing(CommonFieldsMixin):
    title = models.CharField(max_length=255,null=False)
    description = models.TextField(null=False)
    object_metadata = JSONField(default=None)
    ranking = models.IntegerField(null=False)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        default=None)

    class Meta:
        db_table = "favorite_thing"
        ordering = ['created_at']