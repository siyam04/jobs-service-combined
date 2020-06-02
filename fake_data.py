# base importing
import os, django, random
from django.db import connection

# configure settings for project
# need to run this before calling models from application!
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'root.settings')
django.setup()

# faker importing
from faker import Faker
# custom app models importing
from jobs.models import Category, Job, JobTracking

# creating Faker object
fake_data = Faker()

# custom data based on needs
category_list = [
    'IT & Telecommunication', 'Engineer/Architects', 'Production/Operation', 'Accounting/Finance', 'Garments/Textile',
    'Education/Training', 'Medical/Pharma', 'Marketing/Sales'
]

employer_list = [
    'Samsung', 'Brain Station', 'SouthTech','Ador Composite Ltd', 'Texstream Fashion Ltd', 'DreamOnline Limited',
    'AKH Knitting','Rim Leather Ltd.', 'Akij Bakers Ltd.', 'M.N Group', 'Partex Star Group', 'UBF Bridal Ltd.', 'IUBAT',
    'Dikkha Online', 'PRAN-RFL Group', 'Friendship', 'Rupayan Group', 'Paragon Group'
]

status_list = ['FT', 'PT', 'CT']

job_level_list = ['ENT', 'MID', 'EXP']

address_list = [
    'Dhaka(Banani)', 'Chitagong', 'Rangpur, Dinajpur', 'Dhaka(Gulshan)', 'Dhaka(Mirpur)', 'Dhaka(Motijheel)', 'Khulna',
    'Narayanganj', 'Dhaka (Tejgaon Industrial Area)', 'Gazipur'
]

gender_list = ['M', 'F', 'O']

receiving_option_list = ['EM', 'ON', 'HC']

# degree_list = ['BBA', 'BSc', 'Diploma']


# 1st, creating the priority object with fake data
def add_category():
    category = Category.objects.get_or_create(
        name=random.choice(category_list),
    )[0]

    # note: [0] = Usage of get_or_create() method, if priority object already exists then get from first index.
    # if not, then create the priority object.

    # saving priority obj
    category.save()

    # returning priority obj
    return category


# populating the other classes
def populate(n):
    for entry in range(n):
        # 1st, calling priority method for creating priority object first
        category = add_category()

        # 2nd, creating next objects with previously created priority object
        job_obj, job_created = Job.objects.get_or_create(
            job_title=fake_data.job(),
            job_level=random.choice(job_level_list),
            job_responsibilities=fake_data.sentence(),
            job_location=random.choice(address_list),
            no_of_vacancies=random.randint(1, 20),

            category=category,

            employer_id=random.randint(1, 20),
            employer_name=random.choice(employer_list),
            employer_information=fake_data.sentence(),
            employment_status=random.choice(status_list),
            employer_location=random.choice(address_list),

            age=random.randint(20, 45),
            gender=random.choice(gender_list),
            skill=fake_data.sentence(),
            experience=random.randint(1, 10),

            # degree=random.choice(degree_list),

            training=fake_data.sentence(),
            salary=fake_data.random_int(min=10000 , max=80000,step=5000),
            compensation_and_other_benefits=fake_data.sentence(),

            application_deadline=fake_data.date_time(),
            resume_receiving_option=random.choice(receiving_option_list)
        )

        # 3rd, creating another next objects with previously created priority object
        JobTracking.objects.get_or_create(
            job=job_obj or job_created,
            seeker_id=random.randint(1, 20),
            seeker_name=fake_data.name(),
        )


# calling the populate() method
if __name__ == '__main__':
    print("** Populating the Database, Please Wait...")
    populate(5)
    print('** Populating Complete!')



