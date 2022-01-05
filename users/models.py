from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# extend user model, create model 1 to 1 relationship. 1 user <> 1 profile

class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  image = models.ImageField(default='default.jpg', upload_to='profile_pics')

  def __str__(self):
    return f'{self.user.username} Profile'

  def save(self, *args, **kwargs): #save method, method run after save(), exists already in parent but will ad 2 edit
    super().save(*args, **kwargs) # this already happens by default
# to grab image and re-size we need to import pillow and do the following:
    img = Image.open(self.image.path)
    if img.height > 300 or img.width > 300:
      output_size = (300, 300)
      img.thumbnail(output_size)
      img.save(self.image.path)
