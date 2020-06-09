# from django.http import JsonResponse


# def home(request):
#     data = [
#         {
#             "module_name": "JOBS",
#             "providing_api_list":
#                 {
#                     "0. Static APIs (GET)": "http://galib04.pythonanywhere.com/api/choices/",
#                     "1. Create Job (POST)": "http://galib04.pythonanywhere.com/api/job/",
#                     "2. Job List (GET)": "http://galib04.pythonanywhere.com/api/job/?no_of_vacancies=16&category=1&employer_id=11&age=24&gender=M",
#                     "3. Job Details (GET)": "http://galib04.pythonanywhere.com/api/job/1/",
#                     "4. Edit Job (PUT)": "http://galib04.pythonanywhere.com/api/job/1/",
#                     "5. Delete Job (DELETE)": "http://galib04.pythonanywhere.com/api/job/1/",
#                     "6. Apply Job (POST)": "http://galib04.pythonanywhere.com/api/job/apply/1/",
#                     "7. Create Category (POST)": "http://galib04.pythonanywhere.com/api/category/",
#                     "8. Category List (GET)": "http://galib04.pythonanywhere.com/api/category/",
#                     "9. Edit Category (PUT)": "http://galib04.pythonanywhere.com/api/category/1/",
#                     "10. Delete Category (DELETE)": "http://galib04.pythonanywhere.com/api/category/1/",
#                     "11. Applied Jobs by Seeker ID (GET)": "http://galib04.pythonanywhere.com/api/job/seeker/1/",
#                     "12. Posted Job List by Employer ID (GET)": "http://galib04.pythonanywhere.com/api/job/employer/14/",
#                     "13. Job-wise Seeker List (GET)": "http://galib04.pythonanywhere.com/api/job/1/seeker/"
#                 },
#             "expecting_api_list":
#                 {
#                     "EMPLOYER": {"1. Division-wise Jobs Count (GET)": "{{host}}/api/division/"},
#                     "SEEKER": {"1. User Authentication (POST)": "{{host}}/api/..."}
#                 }
#         }
#     ]
#
#     return JsonResponse({"data": data}, status=200)

