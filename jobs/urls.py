from django.urls import path

from .views import (

    StaticChoiceView,
    JobView,
    CategoryView,
    AppliedJobsBySeekerView,
    PostedJobListByEmployerView,
    JobWiseSeekerListView,
)


urlpatterns = [

    # 0. Static APIs (GET): http://127.0.0.1:8000/api/choices/
    path('choices/', StaticChoiceView.as_view()),

    # 1. Create Job (POST): http://127.0.0.1:8000/api/job/
    # 2. Job List (GET)(QS): http://127.0.0.1:8000/api/job/?no_of_vacancies=14&category=1&employer_id=14&age=25&gender=M
    path('job/', JobView.as_view()),

    # 3. Job Details (GET): http://127.0.0.1:8000/api/job/{id}/
    # 4. Edit Job (PUT): http://127.0.0.1:8000/api/job/{id}/
    # 5. Delete Job (DELETE): http://127.0.0.1:8000/api/job/{id}/
    path('job/<int:id>/', JobView.as_view()),

    # 6. Apply Job (POST): http://127.0.0.1:8000/api/job/{id}/apply/
    path('job/<int:id>/apply/', JobView.as_view()),

    # 7. Create Category (POST): http://127.0.0.1:8000/api/category/
    # 8. Category List (GET): http://127.0.0.1:8000/api/category/
    path('category/', CategoryView.as_view()),

    # 9. Edit Category (PUT): http://127.0.0.1:8000/api/category/{id}/
    # 10. Delete Category (DELETE): http://127.0.0.1:8000/api/category/{id}/
    path('category/<int:id>/', CategoryView.as_view()),

    # 11. Applied Jobs by Seeker ID (GET): http://127.0.0.1:8000/api/job/seeker/{id}/
    path('job/seeker/<int:id>/', AppliedJobsBySeekerView.as_view()),

    # 12. Posted Job List by Employer ID (GET): http://127.0.0.1:8000/api/job/employer/{id}/
    path('job/employer/<int:id>/', PostedJobListByEmployerView.as_view()),

    # 13. Job-wise Seeker List (GET): http://127.0.0.1:8000/api/job/{id}/seeker/
    path('job/<int:id>/seeker/', JobWiseSeekerListView.as_view()),

]

