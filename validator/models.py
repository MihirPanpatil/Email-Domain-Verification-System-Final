from django.db import models

# Create your models here.
# validator/models.py
from django.db import models

class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploaded_files/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'File ID: {self.id}'