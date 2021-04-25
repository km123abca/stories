from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Story(models.Model):
	author=models.CharField(max_length=200,null=True)
	finished=models.BooleanField(default=True)
	title= models.CharField(max_length=200,null=True)
	genre= models.CharField(max_length=200,null=True)
	textFileLocation=models.CharField(max_length=200,null=True)
	rating=models.DecimalField(max_digits=2,decimal_places=1,default=6)
	desc=models.CharField(max_length=3000,default='This Story has no description')

	def __str__(self):
		return self.title+' by '+self.author

class Reviewer(models.Model):
	reviewerguy= models.CharField(max_length=200,null=True)
	reviewedstory=models.ForeignKey(Story,on_delete=models.CASCADE)
	rating=models.DecimalField(max_digits=2,decimal_places=1,default=1)
	rreview=models.CharField(max_length=3000,default='No Review')

	def __str__(self):
		return '{guy}\'s opinion on {sto}'.format(guy=this.reviewerguy,sto=this.reviewedstory.title)

