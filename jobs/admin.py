from django.contrib import admin

from .models import (
    Job,
    Category,
    JobTracking,
)


# Category
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['name']
    search_fields = ['id', 'name']
    list_filter = ['id', 'name']


# Job
@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'job_title', 'job_level', 'job_responsibilities', 'job_location', 'no_of_vacancies', 'category',
        'employer_id', 'employer_name', 'employer_information', 'employment_status', 'employer_location',
        'age', 'gender', 'skill', 'experience', 'training', 'salary', 'compensation_and_other_benefits',
        'application_deadline', 'resume_receiving_option'
    ]

    search_fields = [
        'job_title', 'job_level', 'job_responsibilities', 'job_location', 'no_of_vacancies', 'category',
        'employer_name', 'employer_information', 'employment_status', 'employer_location',
        'age', 'gender', 'skill', 'experience', 'training', 'salary', 'compensation_and_other_benefits',
        'application_deadline', 'resume_receiving_option'
    ]

    list_display_links = ['job_title']

    list_filter = [
        'job_title', 'job_level', 'job_responsibilities', 'job_location', 'no_of_vacancies', 'category',
        'employer_id', 'employer_name', 'employer_information', 'employment_status', 'employer_location',
        'age', 'gender', 'skill', 'experience', 'training', 'salary', 'compensation_and_other_benefits',
        'application_deadline', 'resume_receiving_option'
    ]


# JobTracking
@admin.register(JobTracking)
class JobTrackingAdmin(admin.ModelAdmin):
    list_display = ['id', 'job', 'seeker_id', 'seeker_name']

    search_fields = ['id', 'job', 'seeker_id', 'seeker_name']

    list_display_links = ['job']

    list_filter = ['job', 'seeker_id', 'seeker_name']





