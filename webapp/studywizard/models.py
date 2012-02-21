from django.db import models

# Create your models here.
class Stats(models.Model):
	#For app creation
	create_time = models.DateTimeField()
	app_name = models.CharField(max_length=200)
	description = models.TextField()
	contact_email = models.EmailField()

	#Just for us
	creator_name = models.CharField(max_length=200)
	creator_email = models.EmailField()
	org_name = models.CharField(max_length=200)
	location = models.CharField(max_length=200)
	probe_config = models.TextField()