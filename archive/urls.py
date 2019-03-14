from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('scholarships/', views.ScholarshipListView.as_view(), name='scholarships'),
    path('scholarship/<int:pk>', views.ScholarshipDetailView.as_view(), name='scholarship-detail'),
    path('donors/', views.DonorListView.as_view(), name='donors'),
    path('donor/<int:pk>',
         views.DonorDetailView.as_view(), name='donor-detail'),
]


urlpatterns += [
    path('myscholarships/', views.LoanedScholarshipsByUserListView.as_view(), name='my-applied'),
    path(r'applied/', views.LoanedScholarshipsAllListView.as_view(), name='all-applied'),  # Added for challenge
]


# Add URLConf for archival to renew a scholarship.
urlpatterns += [
    path('scholarship/<uuid:pk>/renew/', views.renew_scholarship_archival, name='renew-scholarship-archival'),
]


# Add URLConf to create, update, and delete donors
urlpatterns += [
    path('donor/create/', views.DonorCreate.as_view(), name='donor_create'),
    path('donor/<int:pk>/update/', views.DonorUpdate.as_view(), name='donor_update'),
    path('donor/<int:pk>/delete/', views.DonorDelete.as_view(), name='donor_delete'),
]

# Add URLConf to create, update, and delete scholarships
urlpatterns += [
    path('scholarship/create/', views.ScholarshipCreate.as_view(), name='scholarship_create'),
    path('scholarship/<int:pk>/update/', views.ScholarshipUpdate.as_view(), name='scholarship_update'),
    path('scholarship/<int:pk>/delete/', views.ScholarshipDelete.as_view(), name='scholarship_delete'),
]