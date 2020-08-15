from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Story(models.Model):
	author=models.CharField(max_length=200,null=True)
	title= models.CharField(max_length=200,null=True)
	genre= models.CharField(max_length=200,null=True)
	textFileLocation=models.CharField(max_length=200,null=True)

	def __str__(self):
		return self.title+' by '+self.author

