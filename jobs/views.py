# Python Packages
import json
from pprint import pprint

# Django Packages
from django.views import View
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Custom App
from .models import (
    Job,
    Category,
    JobTracking,
)
from .forms import CategoryForm, JobForm, JobTrackingForm, JobEditForm


# 0. Static APIs (GET): http://127.0.0.1:8000/api/choices/
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


# 1. Create Job (POST): http://127.0.0.1:8000/api/job/
# 2. Job List (GET)(QS): http://127.0.0.1:8000/api/job/?no_of_vacancies=14&category=1&employer_id=14&age=25&gender=M
# 3. Job Details (GET): http://127.0.0.1:8000/api/job/{id}/
# 4. Edit Job (PUT): http://127.0.0.1:8000/api/job/{id}/
# 5. Delete Job (DELETE): http://127.0.0.1:8000/api/job/{id}/
# 6. Apply Job (POST): http://127.0.0.1:8000/api/job/{id}/apply/
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
    job_edit_fields = [
        'job_responsibilities', 'job_location', 'no_of_vacancies', 'employer_information', 'employment_status',
        'age', 'gender', 'skill', 'experience', 'training', 'compensation_and_other_benefits', 'resume_receiving_option'
    ]
    job_tracking_fields = ['seeker_id', 'seeker_name', 'job']
    job_list_querystring = ['no_of_vacancies', 'category', 'employer_id', 'age', 'gender']

    # 1
    # 6
    def post(self, request, id=None):
        # 6. Apply Job
        if id:
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
            body.update({"job": id})

            form = JobTrackingForm(body)

            if form.is_valid():
                instance = form.save()
                return JsonResponse(model_to_dict(instance, fields=self.job_tracking_fields), status=201)
            else:
                return JsonResponse({"errors": form.errors.as_json()}, status=422)

        # 1. Create Job
        else:
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)

            form = JobForm(body)

            if form.is_valid():
                instance = form.save()
                return JsonResponse(model_to_dict(instance, fields=self.job_fields), status=201)
            else:
                return JsonResponse({"errors": form.errors.as_json()}, status=422)

    # 2
    # 3
    def get(self, request, id=None, *args, **kwargs):
        jobs = Job.objects

        # 3. Job Details
        if id:
            query = jobs.get(id=id)
            return JsonResponse(model_to_dict(query, fields=self.job_fields_with_id), status=200)

        # 2. Job List (QueryString)
        else:
            data = {}
            fields = jobs.values(*self.job_fields_with_id)
            for field in self.job_list_querystring:
                data.update({field: request.GET.get(field)})

            jobs = list(fields.filter(**data))

            # pagination
            paginator = Paginator(jobs, 3)
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

    # 4
    def put(self, request, id=None):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        job = Job.objects.get(id=id)

        form = JobEditForm(body, instance=job)

        if form.is_valid():
            instance = form.save()
            return JsonResponse(model_to_dict(instance, fields=self.job_edit_fields), status=200)
        else:
            return JsonResponse({"errors": form.errors.as_json()}, status=422)

    # 5
    def delete(self, request, id=None):
        try:
            job = Job.objects.get(id=id)
            job.delete()
            return JsonResponse({"data": "deleted"}, status=200)
        except Job.DoesNotExist as e:
            return JsonResponse({"errors": f"{e}"}, status=204)


# 7. Create Category (POST): http://127.0.0.1:8000/api/category/
# 8. Category List (GET): http://127.0.0.1:8000/api/category/
# 9. Edit Category (PUT): http://127.0.0.1:8000/api/category/{id}/
# 10. Delete Category (DELETE): http://127.0.0.1:8000/api/category/{id}/
@method_decorator(csrf_exempt, name='dispatch')
class CategoryView(View):
    # 7
    def post(self, request):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        form = CategoryForm(body)

        if form.is_valid():
            instance = form.save()
            return JsonResponse(model_to_dict(instance, fields=["name"]), status=201)
        else:
            return JsonResponse({"errors": form.errors.as_json()}, status=422)

    # 8
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
            return JsonResponse({"data": "not found"}, status=404)

    # 9
    def put(self, request, id=None):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        category = Category.objects.get(id=id)

        form = CategoryForm(body, instance=category)

        if form.is_valid():
            instance = form.save()
            return JsonResponse(model_to_dict(instance, fields=["name"]), status=200)
        else:
            return JsonResponse({"errors": form.errors.as_json()}, status=422)

    # 10
    def delete(self, request, id=None):
        try:
            category = Category.objects.get(id=id)
            category.delete()
            return JsonResponse({"data": "deleted"}, status=200)
        except Category.DoesNotExist as e:
            return JsonResponse({"errors": f"{e}"}, status=204)


# 11. Applied Jobs by Seeker ID (GET): http://127.0.0.1:8000/api/job/seeker/{id}/
@method_decorator(csrf_exempt, name='dispatch')
class AppliedJobsBySeekerView(View):
    # 11
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
            return JsonResponse({"data": "not found"}, status=404)


# 12. Posted Job List by Employer ID (GET): http://127.0.0.1:8000/api/job/employer/{id}/
@method_decorator(csrf_exempt, name='dispatch')
class PostedJobListByEmployerView(View):
    # 12
    def get(self, request, id=None):
        tracking_query = Job.objects.filter(employer_id=id)

        data = []

        for element in tracking_query:
            data.append(
                {"job_title": element.job_title}
            )

        if data:
            return JsonResponse({"data": data}, status=200)
        else:
            return JsonResponse({"data": "not found"}, status=404)


# 13. Job-wise Seeker List (GET): http://127.0.0.1:8000/api/job/{id}/seeker/
@method_decorator(csrf_exempt, name='dispatch')
class JobWiseSeekerListView(View):
    # 13
    def get(self, request, id=None):
        tracking_query = JobTracking.objects.filter(job=id)

        data = []

        for element in tracking_query:
            data.append(
                {"seeker_name": element.seeker_name}
            )

        if data:
            return JsonResponse({"data": data}, status=200)
        else:
            return JsonResponse({"data": "not found"}, status=404)




