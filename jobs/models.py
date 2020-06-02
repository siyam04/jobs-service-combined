from django.db import models
from django.utils.translation import gettext_lazy as _


# Categories Table
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        # ordering = ['-id']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


# Job Table
class Job(models.Model):
    """Choices"""
    class EmploymentStatus(models.TextChoices):
        FULL_TIME = 'FT', _('FULL_TIME')
        PART_TIME = 'PT', _('PART_TIME')
        CONTRACTUAL = 'CT', _('CONTRACTUAL')

    class ResumeReceivingOption(models.TextChoices):
        EMAIL = 'EM', _('EMAIL')
        ONLINE = 'ON', _('ONLINE')
        HARD_COPY = 'HC', _('HARD_COPY')

    class JobLevel(models.TextChoices):
        ENTRY = 'ENT', _('ENTRY')
        MID = 'MID', _('MID')
        EXPERT = 'EXP', _('EXPERT')

    class Gender(models.TextChoices):
        MALE = 'M', _('MALE')
        FEMALE = 'F', _('FEMALE')
        OTHERS = 'O', _('OTHERS')

    # class Degree(models.TextChoices):
    #     BBA = 'BBA', _('BBA')
    #     BSc = 'BSc', _('BSc')
    #     DIPLOMA = 'Diploma', _('DIPLOMA')

    job_title = models.CharField(max_length=200, null=True, blank=True)
    job_level = models.CharField(max_length=20, choices=JobLevel.choices, null=True, blank=True)
    job_responsibilities = models.TextField(max_length=2000, null=True, blank=True)
    job_location = models.CharField(max_length=100, null=True, blank=True)
    no_of_vacancies = models.PositiveSmallIntegerField(null=True, blank=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)

    employer_id = models.PositiveSmallIntegerField(null=True, blank=True)
    employer_name = models.CharField(max_length=200, null=True, blank=True)
    employer_information = models.TextField(max_length=500, null=True, blank=True)
    employment_status = models.CharField(max_length=20, choices=EmploymentStatus.choices, null=True, blank=True)
    employer_location = models.CharField(max_length=100, null=True, blank=True)

    age = models.PositiveSmallIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=20, choices=Gender.choices, null=True, blank=True)
    skill = models.TextField(max_length=1000, null=True, blank=True)
    experience = models.PositiveSmallIntegerField(null=True, blank=True)

    # degree = models.CharField(max_length=20, choices=Degree.choices, null=True, blank=True)

    training = models.TextField(max_length=500, null=True, blank=True)
    salary = models.FloatField(default=0.00, null=True, blank=True)
    compensation_and_other_benefits = models.TextField(max_length=500, null=True, blank=True)

    application_deadline = models.DateTimeField(auto_now_add=True, editable=False, null=True, blank=True)
    resume_receiving_option = models.CharField(max_length=20, choices=ResumeReceivingOption.choices, default=ResumeReceivingOption.EMAIL, null=True, blank=True)

    class Meta:
        # ordering = ['-id']
        verbose_name_plural = 'Jobs'

    def __str__(self):
        return self.job_title


# JobTracking Table
class JobTracking(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, null=True, blank=True)
    seeker_id = models.PositiveSmallIntegerField(null=True, blank=True)
    seeker_name = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        # ordering = ['-id']
        verbose_name_plural = 'Job tracking'
        unique_together = ['job', 'seeker_id']

    def __str__(self):
        return str(self.seeker_name)

        # if self.job.job_title:
        #     return self.job.job_title
        #     # return '{}, {}, {}'.format(self.job.job_title, self.seeker_name, self.job.employer_name)
        # else:
        #     return self.seeker_name



