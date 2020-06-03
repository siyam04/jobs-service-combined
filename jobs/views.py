# Python Packages
import json
from pprint import pprint

# Django Packages
from django.views import View
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.contrib.auth import authenticate
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, redirect, get_object_or_404

# Custom App
from .models import (
    Job,
    Category,
    JobTracking,
)
from .forms import CategoryForm, JobForm, JobTrackingForm


# 0. Static APIs: http://127.0.0.1:8000/api/choices/
@method_decorator(csrf_exempt, name='dispatch')
class StaticChoiceView(View):
    def get(self, request):
        data = [
            {
                "gender": dict(Job.Gender.choices),
                "employment_status": dict(Job.EmploymentStatus.choices),
                "job_level": dict(Job.JobLevel.choices),
                "resume_receiving_option": dict(Job.ResumeReceivingOption.choices)
            }
        ]
        return JsonResponse({"data": data}, status=200)


# 1. Create Job: http://127.0.0.1:8000/api/job/ (POST)
# 2. Job List: http://127.0.0.1:8000/api/job/ (GET)
# 3. Job Details: http://127.0.0.1:8000/api/job/id/ (GET)
# 13. Apply Job: http://127.0.0.1:8000/api/job/apply/id/ (POST)
@method_decorator(csrf_exempt, name='dispatch')
class JobView(View):
    job_fields = [
        'job_title', 'job_level', 'job_responsibilities', 'job_location', 'no_of_vacancies', 'category',
        'employer_id', 'employer_name', 'employer_information', 'employment_status', 'employer_location',
        'age', 'gender', 'skill', 'experience', 'training', 'salary', 'compensation_and_other_benefits',
        'application_deadline', 'resume_receiving_option'
    ]
    job_fields_with_id = [
        'id', 'job_title', 'job_level', 'job_responsibilities', 'job_location', 'no_of_vacancies', 'category',
        'employer_id', 'employer_name', 'employer_information', 'employment_status', 'employer_location',
        'age', 'gender', 'skill', 'experience', 'training', 'salary', 'compensation_and_other_benefits',
        'application_deadline', 'resume_receiving_option'
    ]
    job_tracking_fields = ['seeker_id', 'seeker_name', 'job']
    job_list_querystring = ['no_of_vacancies', 'category', 'employer_id', 'age', 'gender']

    # 1
    # 13
    def post(self, request, id=None, *args, **kwargs):
        # 13. Apply Job
        if id:
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            body.update({"job": id})

            form = JobTrackingForm(body)

            if form.is_valid():
                instance = form.save()
                return JsonResponse(model_to_dict(instance, fields=self.job_tracking_fields), status=201)
                # return JsonResponse(model_to_dict(instance, fields=[field.name for field in instance._meta.fields]))
                # return JsonResponse(model_to_dict(instance, fields=["seeker_name", "seeker_id"]))
            else:
                return JsonResponse({"errors": form.errors}, status=422)

        # 1. Create Job
        else:
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)

            form = JobForm(body)

            if form.is_valid():
                instance = form.save()
                return JsonResponse(model_to_dict(instance, fields=self.job_fields), status=201)
            else:
                return JsonResponse({"errors": form.errors}, status=422)

    # 2
    # 3
    def get(self, request, id=None, *args, **kwargs):
        jobs = Job.objects

        # 3. Job Details
        if id:
            query = jobs.get(id=id)
            return JsonResponse(model_to_dict(query, fields=self.job_fields_with_id), status=200)

        # 2. Job List
        else:
            data = {}
            fields = jobs.values(*self.job_fields_with_id)
            for field in self.job_list_querystring:
                data.update({field: request.GET.get(field)})

            jobs = list(fields.filter(**data))
            data = list(jobs)

            # pagination
            paginator = Paginator(data, 3)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            context = {
                "data": list(page_obj),  # or, list(page_obj.object_list)
                "pagination": {
                    "total_pages": page_obj.paginator.num_pages,
                    "current_page_number": page_obj.number,
                    "previous": page_obj.has_previous() > 0 and page_obj.previous_page_number() or None,
                    "next": page_obj.has_next() > 0 and page_obj.next_page_number() or None,
                }
            }

            return JsonResponse(context)


# 4. Edit Job : http://127.0.0.1:8000/api/job/id/ (PUT)
# 5. Delete Job: http://127.0.0.1:8000/api/job/id/ (DELETE)
@method_decorator(csrf_exempt, name='dispatch')
class JobEditDeleteView(View):
    # 4
    def put(self, request, id=None):
        try:
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)

            job_title = body['job_title']
            job = get_object_or_404(Job, id=id)
            job.job_title = job_title
            job.save()

            return JsonResponse({"message": "Updated!"}, status=201)

        except Job.DoesNotExist as e:
            return JsonResponse({"message": e}, status=404)

    # 5
    def delete(self, request, id=None):
        job = get_object_or_404(Job, id=id)
        if job:
            job.delete()
            return JsonResponse({"message": "Deleted!"}, status=200)
        else:
            return JsonResponse({"message": "No Content"}, status=204)


# 6. Create Category : http://127.0.0.1:8000/api/category/create/ (POST)
# 7. Category List: http://127.0.0.1:8000/api/category/ (GET)
@method_decorator(csrf_exempt, name='dispatch')
class CategoryView(View):
    # 6
    def post(self, request):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        form = CategoryForm(body)

        if form.is_valid():
            instance = form.save()
            return JsonResponse(model_to_dict(instance, fields=["name"]))
        else:
            return JsonResponse({"errors": form.errors}, status=422)

        # # assigning parsed data
        # name = body['name']
        #
        # # if data available
        # if name:
        #     # create category
        #     Category.objects.create(name=name)
        #
        #     # return api response
        #     return JsonResponse({'message': 'Created!'}, status=201)
        #
        # # if data not available
        # else:
        #     return JsonResponse({"message": "Not Found!"}, status=404)

    # 7
    def get(self, request):
        queryset = Category.objects.all()

        data = []

        for element in queryset:
            job_count = Job.objects.filter(category__id=element.id).count()

            data.append(
                {"id": element.id, "name": element.name, "job_count": job_count}
            )

        if data:
            return JsonResponse({"data": data}, status=200)
        else:
            return JsonResponse({"data": "no content"}, status=204)


# 8. Edit Category: http://127.0.0.1:8000/api/category/id/ (PUT)
# 9. Delete Category: http://127.0.0.1:8000/api/category/id/ (DELETE)
@method_decorator(csrf_exempt, name='dispatch')
class CategoryEditDeleteView(View):
    # 8
    def put(self, request, id=None):
        try:
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            name = body['name']

            category = get_object_or_404(Category, id=id)
            category.name = name
            category.save()
            return JsonResponse({"name": category.name}, status=201)

        except Category.DoesNotExist as e:
            return JsonResponse({"errors": e}, status=404)

    # 9
    def delete(self, request, id=None):
        try:
            category = Category.objects.get(id=id)
            category.delete()
            return JsonResponse({"data": "deleted"}, status=200)
        except Category.DoesNotExist as e:
            return JsonResponse({"errors": f"{e}"}, status=404)


# 10. Applied Jobs by Seeker: http://127.0.0.1:8000/api/job/seeker/id/ (GET)
@method_decorator(csrf_exempt, name='dispatch')
class AppliedJobsBySeekerIDView(View):
    # 10
    def get(self, request, id=None):
        tracking_query = JobTracking.objects.filter(seeker_id=id)

        data = []

        for element in tracking_query:
            data.append(
                {"job_title": element.job.job_title}
            )

        if data:
            return JsonResponse({"data": data}, status=200)
        else:
            return JsonResponse({"message": "Not Found!"}, status=404)


# 11. Posted Job List by Employer:: http://127.0.0.1:8000/api/job/employer/ (GET) (Need to add QS)
@method_decorator(csrf_exempt, name='dispatch')
class PostedJobListByEmployerView(View):
    # 11
    def get(self, request):
        tracking_query = Job.objects.filter(employer_name='Texstream Fashion Ltd')

        data = []

        for element in tracking_query:
            data.append(
                {"job_title": element.job_title}
            )

        if data:
            return JsonResponse({"data": data}, status=200)
        else:
            return JsonResponse({"message": "Not Found!"}, status=404)


# 12. Job-wise Seeker List: http://127.0.0.1:8000/api/job/id/seeker/ (GET)
@method_decorator(csrf_exempt, name='dispatch')
class JobWiseSeekerListView(View):
    # 12
    def get(self, request, id=None):
        queryset = JobTracking.objects.filter(job=id)

        data = []

        for element in queryset:
            data.append(
                {"seeker_name": element.seeker_name}
            )

        if data:
            return JsonResponse({"data": data}, status=200)
        else:
            return JsonResponse({"message": "Not Found!"}, status=404)
