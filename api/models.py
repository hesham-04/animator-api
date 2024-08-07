from django.db import models

class Media(models.Model):
    driving_video = models.FileField(upload_to='driving_videos/')
    input_image = models.ImageField(upload_to='input_images/')
    output_video = models.FileField(upload_to='output_animations/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'Animation {self.id}'
