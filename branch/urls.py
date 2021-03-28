from django.urls import path
from .views import Branches_view,Branch_detailView,Truck_view,branch_trucks,Truck_detailView,OtherBranches,BranchWork,TrackInfo,getTripsInfo
urlpatterns = [
    path('branches/',Branches_view.as_view()),
    path('branch/<int:pk>',Branch_detailView.as_view()),
    path('trucks/',Truck_view.as_view()),
    path('truck/<int:pk>',Truck_detailView.as_view()),
    path('branch-trucks/',branch_trucks.as_view()),
    path('other-branches/',OtherBranches.as_view()),
    path('add-work/',BranchWork.as_view()),
    path('track/<int:pk>',TrackInfo.as_view()),
    path('trips/',getTripsInfo.as_view()),
]