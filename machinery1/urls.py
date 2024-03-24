from django.urls import path
from machinery1 import views

app_name = "machinery1"


urlpatterns = [

    #path('', views.home_view, name='home'),
    path('machines/', views.machine_list_view, name='machine-list'),
    #path('job/<int:id>/', views.single_job_view, name='single-job'),
    path('machine/create/', views.create_machine_view, name='create-machine'),
    path('machines/<int:id>/', views.single_machine_view, name='single-machine'),
    path('apply-machine/<int:id>/', views.apply_machine_view, name='apply-machine'),
    path('bookmark-machine/<int:id>/', views.machine_bookmark_view, name='bookmark-machine'),
    #path('contact/', views.single_machine_view, name='contact'),
    #path('result/', views.search_result_view, name='search_result'),
    #path('dashboard/', views.dashboard_view, name='dashboard'),
    #path('dashboard/employer/job/<int:id>/applicants/', views.all_applicants_view, name='applicants'),
    path('machineadmin/employer/machine/<int:id>/clients/', views.all_clients_view, name='clients'),
    path('machineadmin/', views.machineadmin_list_view, name='my-machines'),
    path('machineadmin/employer/machine/edit/<int:id>', views.machine_edit_view, name='edit-machine'),
    path('machineadmin/client/<int:id>/', views.client_details_view, name='client-details'),
    #path('dashboard/employer/applicant/<int:id>/', views.applicant_details_view, name='applicant-details'),
    path('machineadmin/employer/make-unavailable/<int:id>/', views.make_unavailable_machine_view, name='make-unavailable'),
    path('machineadmin/employer/delete/<int:id>/', views.delete_machine_view, name='delete'),
    path('machineadmin/employee/delete-machinebookmark/<int:id>/', views.delete_bookmark_view, name='delete-machinebookmark'),


]
