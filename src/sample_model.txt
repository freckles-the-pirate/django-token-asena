from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.

class MyModel(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        abstract = False
        app_label = _("mymodel")
        verbose_name = _("mymodel")

