
# models.py
from django.db import models

class HarvestedData(models.Model):
    file_name = models.CharField(max_length=255)
    file_content = models.JSONField()  # Store file content as JSON or other relevant format
    upload_date = models.DateTimeField(auto_now_add=True)
