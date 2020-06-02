from django.urls import path

from .views import (

    StaticChoiceView,

    JobView,
    JobEditDeleteView,

    CategoryView,
    CategoryEditDeleteView,

    AppliedJobsBySeekerIDView,
    PostedJobListByEmployerView,

    JobWiseSeekerListView,

)


urlpatterns = [

    # Static APIs: http://127.0.0.1:8000/api/choices/ (GET)
    path('choices/', StaticChoiceView.as_view()),

    # 1. Create Job: http://127.0.0.1:8000/api/job/ (POST)
    # 2. Job List: http://127.0.0.1:8000/api/job/ (GET)
    path('job/', JobView.as_view()),

    # 13. Apply Job: http://127.0.0.1:8000/api/job/apply/id/ (POST)
    path('job/apply/<int:id>/', JobView.as_view()),

    # 3. Job Details: http://127.0.0.1:8000/api/job/id/ (GET)
    path('job/<int:id>/', JobView.as_view()),


    # 4. Edit Job : http://127.0.0.1:8000/api/job/id/ (PUT)
    # 5. Delete Job: http://127.0.0.1:8000/api/job/id/ (DELETE)
    path('job/<int:id>/', JobEditDeleteView.as_view()),

    # 6. Create Category : http://127.0.0.1:8000/api/category/ (POST)
    # 7. Category List: http://127.0.0.1:8000/api/category/ (GET)
    path('category/', CategoryView.as_view()),

    # 8. Edit Category: http://127.0.0.1:8000/api/category/id/ (PUT)
    # 9. Delete Category: http://127.0.0.1:8000/api/category/id/ (DELETE)
    path('category/<int:id>/', CategoryEditDeleteView.as_view()),

    # 10. Applied Jobs by Seeker ID: http://127.0.0.1:8000/api/job/seeker/id/ (GET)
    path('job/seeker/<int:id>/', AppliedJobsBySeekerIDView.as_view()),

    # 11. Posted Job List by Employer:: http://127.0.0.1:8000/api/job/employer/ (GET)
    path('job/employer/', PostedJobListByEmployerView.as_view()),

    # 12. Job-wise Seeker List: http://127.0.0.1:8000/api/job/id/seeker/ (GET)
    path('job/<int:id>/seeker/', JobWiseSeekerListView.as_view()),

]

