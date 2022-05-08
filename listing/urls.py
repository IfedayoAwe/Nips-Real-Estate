from django.urls import path
from . views import ManageListingView, ListingDetailView, ListingsView, SearchListingView


urlpatterns = [
    path('manage', ManageListingView.as_view()),
    path('manage/<int:pk>/', ManageListingView.as_view()),
    path('detail', ListingDetailView.as_view()),
    path('get-listings', ListingsView.as_view()),
    path('search', SearchListingView.as_view()),
]