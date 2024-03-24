import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE','job.settings')

import django

django.setup()

import random

from jobapp.models import Job

from faker import Faker

fake = Faker()


def populate(value):
	for i in range(value):
		user = random.randint(1,188)
		title = 'Design'
		location = random.randint(1,47)
		salary = random.randint(5000,100000)
		company_name = fake.company()
		description = fake.text()
		obj = Job.objects.get_or_create(user=user,title=title,location=location,salary=salary,company_name=company_name,description=description)
	
		
def main():
	no = int(input("how many records do you want to send"))
	populate(no)
	
	
if __name__ == "__main__":
	main()
	
