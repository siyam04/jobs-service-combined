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
from .forms import JobTrackingForm


# Static APIs: http://127.0.0.1:8000/api/choices/
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
    job_fields = ['id', 'job_title', 'no_of_vacancies', 'category']
    list_querystring = ['no_of_vacancies', 'category']
    list_details = ['age', 'category']
    job_tracking_fields = ['seeker_id', 'seeker_name', 'job']

    # 1
    def post(self, request, id=None, *args, **kwargs):
        if id:
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            body.update({"job": id})

            form = JobTrackingForm(body)

            if form.is_valid():
                instance = form.save()

                return JsonResponse(model_to_dict(instance, fields=self.job_tracking_fields))
                # return JsonResponse(model_to_dict(instance, fields=[field.name for field in instance._meta.fields]))
                # return JsonResponse(model_to_dict(instance, fields=["seeker_name", "seeker_id"]))
            else:
                return JsonResponse({"errors": form.errors}, status=402)

        else:
            # ToDo: ModelForm validation, params spreading for getting body data and create(), prevent duplicate obj creation
            # ToDo: master testing
            # parsing body data
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)

            # assigning parsed data
            job_title = body['job_title']
            job_level = body['job_level']
            job_responsibilities = body['job_responsibilities']
            job_location = body['job_location']
            no_of_vacancies = body['no_of_vacancies']

            # getting category object by body data
            try:
                category_id = json.dumps(body['category'])
                category = Category.objects.get(id=category_id)
            except Exception as e:
                return JsonResponse({"message": e})

            employer_id = body['employer_id']
            employer_name = body['employer_name']
            employer_information = body['employer_information']
            employment_status = body['employment_status']
            employer_location = body['employer_location']

            age = body['age']
            gender = body['gender']
            skill = body['skill']
            experience = body['experience']
            # degree = body['degree']
            training = body['training']
            salary = body['salary']
            compensation_and_other_benefits = body['compensation_and_other_benefits']

            application_deadline = body['application_deadline']
            resume_receiving_option = body['resume_receiving_option']

            # if data available
            if job_title and job_level and job_responsibilities and job_location and no_of_vacancies and category and employer_id and employer_name and employer_information and employment_status and employer_location and age and gender and skill and experience and training and salary and compensation_and_other_benefits and application_deadline and resume_receiving_option:

                # body_params = [
                #     job_title, job_level, job_responsibilities, job_location, no_of_vacancies,
                #     employer_id, employer_name, employer_information, employment_status, employer_location,
                #     age, gender, skill, experience, training, salary, compensation_and_other_benefits,
                #     application_deadline, resume_receiving_option
                # ]

                # create job
                Job.objects.create(
                    job_title=job_title,
                    job_level=job_level,
                    job_responsibilities=job_responsibilities,
                    job_location=job_location,
                    no_of_vacancies=no_of_vacancies,

                    category=category,

                    employer_id=employer_id,
                    employer_name=employer_name,
                    employer_information=employer_information,
                    employment_status=employment_status,
                    employer_location=employer_location,

                    age=age,
                    gender=gender,
                    skill=skill,
                    experience=experience,
                    # degree=degree,
                    training=training,
                    salary=salary,
                    compensation_and_other_benefits=compensation_and_other_benefits,

                    application_deadline=application_deadline,
                    resume_receiving_option=resume_receiving_option,
                )

                # return api response
                return JsonResponse({'message': 'Job Created!'}, status=201, safe=False)

            # if data not available
            else:
                return JsonResponse({"message": "Not Found!"}, status=404, safe=False)

    # 2
    # 3
    def get(self, request, id=None):
        queryset = Job.objects

        if id:
            job_detail = queryset.get(id=id)
            data = {
                "id": job_detail.id,
                "job_title": job_detail.job_title,
                "job_level": job_detail.job_level,
                "job_responsibilities": job_detail.job_responsibilities,
            }
        else:
            # list search
            job_list = queryset.values(*self.list_fields)
            data = list(job_list)

            # QS
            ## job_list = queryset.values(*self.list_querystring)
            # job_list = queryset.values(*self.list_fields)
            # no_of_vacancies = request.GET.get('no_of_vacancies')
            # category = request.GET.get('category')
            # jobs = list(job_list.filter(no_of_vacancies=no_of_vacancies, category=category))
            # data = list(jobs)

            # pagination
            paginator = Paginator(data, 5)
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

        return JsonResponse({"data": data}, status=200)


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
        # getting api data from Employer module
        # parsing body data
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        # assigning parsed data
        name = body['name']

        # if data available
        if name:
            # create category
            Category.objects.create(name=name)

            # return api response
            return JsonResponse({'message': 'Created!'}, status=201)

        # if data not available
        else:
            return JsonResponse({"message": "Not Found!"}, status=404)

    # 7
    def get(self, request):
        category_queryset = Category.objects.all()

        data = []

        for element in category_queryset:
            job_count = Job.objects.filter(category__id=element.id).count()

            data.append(
                {"id": element.id, "name": element.name, "job_count": job_count}
            )

        if data:
            return JsonResponse({"categories": data}, status=200, safe=False)
        else:
            return JsonResponse({"message": "Not Found!"}, status=404, safe=False)


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

            return JsonResponse({"message": "Updated!"}, status=201, safe=False)

        except Category.DoesNotExist as e:
            return JsonResponse({"message": e}, status=404, safe=False)

    # 9
    def delete(self, request, id=None):
        category = get_object_or_404(Category, id=id)
        if category:
            category.delete()
            return JsonResponse({"message": "Deleted!"}, status=200)
        else:
            return JsonResponse({"message": "No Content"}, status=204)


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