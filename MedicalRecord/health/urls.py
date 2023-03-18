from django.urls import path
from health import views

urlpatterns = [
    
    path("", views.index, name='index'),
    path("patient/", views.patient, name='patient'),
    path("signup", views.signup, name='signup'),
    path("check_address/", views.check_address, name='check_address'),
    path("doctor/", views.doctor, name='doctor'),
    path("adddoctor/", views.adddoctor, name='adddoctor'),
    path("viewcampaigns/", views.viewcampaigns, name='viewcampaigns'),
    path("researchcompany/", views.researchcompany, name='researchcompany'),   
    path("createcampaign/", views.createcampaign, name='createcampaign'),
    path("applyforcampaign/", views.applyforcampaign, name='applyforcampaign'),
    path("addpatient/", views.addpatient, name='addpatient'),
    path("addmedrecord/", views.addmedrecord, name='addmedrecord'),
    path("viewmedrecord/", views.viewmedrecord, name='viewmedrecord'),
]