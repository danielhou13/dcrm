from django.db import models
from PIL import Image

IMAGE_SIZE = 400


# Create your models here.
class Record(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=10)
    pic = models.ImageField(default="default.jpg", upload_to="record_pics")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.pic.path)

        if img.height > IMAGE_SIZE or img.width > IMAGE_SIZE:
            output_size = (IMAGE_SIZE, IMAGE_SIZE)
            img.thumbnail(output_size)
            img.save(self.pic.path)
