from django.db import models
from django.conf import settings

class Photo(models.Model):
    file = models.ImageField(upload_to='profile_img/')
    description = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)

    class Meta:
        verbose_name = 'photo'
        verbose_name_plural = 'photos'

    def save(self, *args, **kwargs):
        try:
            photo = Photo.objects.get(id=self.id)
            if photo.file != self.file:
                photo.file.delete()
        except: pass
        super(Photo, self).save(*args, **kwargs)