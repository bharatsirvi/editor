from django.db import models
from django.utils import timezone     
# Create your models here.
class ImageFile(models.Model):
    img = models.ImageField(upload_to='upload/',null=False,blank=False)
    created_at = models.DateTimeField(default=timezone.now)
    processed_img = models.ImageField(upload_to='processed/',null=True, blank=True)
    
    