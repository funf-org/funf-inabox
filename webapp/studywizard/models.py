# 
# Funf: Open Sensing Framework
# Copyright (C) 2010-2011 Nadav Aharony, Wei Pan, Alex Pentland.
# Acknowledgments: Alan Gardner
# Contact: nadav@media.mit.edu
# 
# This file is part of Funf.
# 
# Funf is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.
# 
# Funf is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public
# License along with Funf. If not, see <http://www.gnu.org/licenses/>.
# 
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