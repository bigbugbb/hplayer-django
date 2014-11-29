from django.db import models
from separatedvaluesfield.models import SeparatedValuesField


class VideoManager(models.Manager):
    def create_video(self, name, image, url, format):
        video = self.create(name=name, image=image, url=url, format=format)
        return video

class AudioManager(models.Manager):
    def create_audio(self, name, url, intro, duration):
        audio = self.create(name=name, url=url, intro=intro, duration=duration)
        return audio

class CartoonManager(models.Manager):
	def create_cartoon(self, name, image, urls):
		cartoon = self.create(name=name, image=image, urls=urls)
		return cartoon

class Video(models.Model):

	def __str__(self):
		return self.name

	name   = models.TextField(unique=True)
	image  = models.TextField()
	url    = models.TextField()
	format = models.CharField(max_length=16)

	objects = VideoManager()

class Audio(models.Model):

	def __str__(self):
		return self.name

	name     = models.TextField(unique=True)
	url      = models.TextField()
	intro    = models.TextField()
	duration = models.CharField(max_length=32)

	objects = AudioManager()

class Cartoon(models.Model):

	def __str__(self):
		return self.name

	name  = models.TextField(unique=True)
	image = models.TextField()
	urls  = SeparatedValuesField(token=',')

	objects = CartoonManager()

