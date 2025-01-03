from django.urls import path
from . import views
from .views import generate_pdf

app_name = 'inout'
urlpatterns = [
    path('report/', views.WorkLogReportView.as_view(), name='worklog_report'),
    path("upload-worklog/", views.upload_worklog, name="upload_worklog"),
    path('generate-pdf/', generate_pdf, name='generate_pdf'),
]
