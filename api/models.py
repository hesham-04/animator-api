from django.db import models
from PIL import Image

class Media(models.Model):
    driving_video = models.FileField(upload_to='driving_videos/')
    input_image = models.ImageField(upload_to='input_images/')
    output_video = models.FileField(upload_to='output_animations/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.input_image:
            try:
                print(f"Image path: {self.input_image.path}")  # Debugging
                img = Image.open(self.input_image.path)
                img = img.resize((512, 512), Image.ANTIALIAS)
                img.save(self.input_image.path, format=img.format)
            except Exception as e:
                print(f"Error processing image: {e}")  # Debugging
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Animation {self.id}'
