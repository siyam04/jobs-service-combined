from django.http import JsonResponse


def home(request):
    data = [
        {
            "test": "Test",
            "test2": "Test-2",
            "test3": "Test-3",
            "module_name": "JOBS",
            "providing_api_list":
                {
                    "0. Static APIs (GET)": "http://galib04.pythonanywhere.com/api/choices/",
                    "1. Create Job (POST)": "http://galib04.pythonanywhere.com/api/job/",
                    "2. Job List (GET)": "http://galib04.pythonanywhere.com/api/job/",
                    "3. Job Details (GET)": "http://galib04.pythonanywhere.com/api/job/1/",
                    "4. Edit Job (PUT)": "http://galib04.pythonanywhere.com/api/job/1/",
                    "5. Delete Job (DELETE)": "http://galib04.pythonanywhere.com/api/job/1/",
                    "6. Create Category (POST)": "http://galib04.pythonanywhere.com/api/category/",
                    "7. Category List (GET)": "http://galib04.pythonanywhere.com/api/category/",
                    "8. Edit Category (PUT)": "http://galib04.pythonanywhere.com/api/category/1/",
                    "9. Delete Category (DELETE)": "http://galib04.pythonanywhere.com/api/category/1/",
                    "10. Applied Jobs by Seeker ID (GET)": "http://galib04.pythonanywhere.com/api/job/seeker/1/",
                    "11. Posted Job List by Employer (GET)": "http://galib04.pythonanywhere.com/api/job/employer/",
                    "12. Job-wise Seeker List (GET)": "http://galib04.pythonanywhere.com/api/job/1/seeker/",
                    "13. Apply Job (POST)": "http://galib04.pythonanywhere.com/api/job/apply/1/"
                },
            "expecting_api_list":
                {
                    "EMPLOYER": {"1. Division-wise Jobs Count (GET)": "{{host}}/api/division/"},
                    "SEEKER": {"1. User Authentication (POST)": "{{host}}/api/..."}
                }
        }
    ]

    return JsonResponse({"data": data}, status=200)

