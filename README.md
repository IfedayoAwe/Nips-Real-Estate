# The-Nips-Crib

## Description

This repository contains the the code that each file in the project directory of building the Real Estate company website "Nips-Real-Estate" with a full regstration and authentication system, this website makes implementation of multiple user levels like an is_superuser who has permissions to make altererations to any data in the database, is_realtor who are admins and have CRUD permissions on listings (real estate post on the website) to the database and norrmal users who can only view and comment on listings. This website uses two separate postgresql database: the 'user' database for managing all users and 'listing' database for managing listings and also custom made routers in the user app for the user data and in the listing app for the listing data respectively to enable proper read, write, relation and migration to the database. Custom ModelAdmin classes were also written to have full permissions over all data were implemented in the admin.py file of each app. When realtors create listings, they could be published immediately or be saved to a draft where only the creator of that listing can view it and then publish it when wanted. Unathorized users are able to view the home page (ListingView) which contains all the published listings by all realtors but cannot access the detail page of any listing, Normal users who are registered and logged in can view both the home page and the detail page of any published listing. The project is designed as intended for usage in a production environment either with templates or as api endpoints using token authentication.

## Features

* Authentication: This consists of a user registration and login feature for both realtor users and normal users. In the user directory of this repository consists of a RegisterView() and RetrieveUserView() in the views.py file. This is to register new users and to retrieve the users respectively.

* CRUD functions on Listings: Class based views were used in the listing/views.py file to implement CRUD operations on listings for realtor users. Non registered users as well as loggedout users can only view the home page, you do not need a token to access these pages. Logged in users can view both the home and detail page of listings.
When realtor users create listings, they have sale_type choices which could either be FOR_SALE or FOR_RENT, home_type choices which could be HOUSE, CONDO or TOWNHOUSE, and is_published which could either True or False

* To delete a user where by all listings associated with that user would be implemeted, Django does not support cross database relationships so this was implemeted with a helper function in the delete.py file of the listing app. Note: There is no user delete API endpoint so this feature can only be accessed through the admin panel, you could always create an endpoint for this feature and it would work accordingly.

* Search: every logged in user can make a full text search on listings.

## Language
The Nips Crib was built in Python using the Django framework and also the Django Rest framework for the corresponding API VIEWS.


## Dependencies
asgiref==3.5.0
Django==4.0.4
django-cleanup==6.0.0
djangorestframework==3.13.1
djangorestframework-simplejwt==5.1.0
Pillow==9.1.0
psycopg2==2.9.3
PyJWT==2.3.0
pytz==2022.1
sqlparse==0.4.2
tzdata==2022.1

## Post Man Documentation
A list of the endpoints and the functions they implement can be found inside every app folder.

app_name = 'user'

urlpatterns = [
    path('register', RegisterView.as_view()),
    path('getuser', RetrieveUserView.as_view()),
]

app_name = 'listing'

urlpatterns = [
    path('manage', ManageListingView.as_view()),
    path('manage/<int:pk>/', ManageListingView.as_view()),
    path('detail', ListingDetailView.as_view()),
    path('get-listings', ListingsView.as_view()),
    path('search', SearchListingView.as_view()),
]

1. The RegisterView creates new users, no authentication is needed to create a new user. Keys: name, email, password, re_password, is_realtor and the respective values are required. pass True to create a realto user and False to create a normal user
2. The RetrieveUserView retrieves a user, pass the token of that user as a Bearer token
3. When using the ManageListingView, to create a new listing the keys: title, slug, address, city, state, zipcode, description, price, bedrooms, bathrooms, sale_type, home_type, main_photo, photo_1, photo_2, photo_3, is_published and the respective values to those keys.
note: when passing sale_type your value options are "FOR_SALE" and "FOR_RENT", when passing home_type your value options are "HOUSE", "CONDO" and "TOWNHOUSE", when passing is_published your value options are "True" and "False".
4. When using the ManageListingView, to retrieve listings, the authentication token of a realtor is needed. If a slug is not passed then all the listings made by that user would be retrieved both published and not published and if a slug is passed then only that listing would be retrieved.
5. To update a listing, an authentication token and the various keys must be provided, an id of a listing created by the owner of that authentication token must also be passed in the request.
6. To publish listings in draft or to remove it from the home view to the draft, a patch request would be sent, the id of that listing in the request, the key is_published and the value True or False must be passed.
7. To delete a listing, an authentication token must be provided and the id of the listing must be passed in the request.
8. When using the ListingDetailView, only authenticated accounts can view the detail page of a published listing, an id of the listing must be passed in the request.
9. When using the ListingView, no authentication token is required as visitors can view the home page of listings.
10. When using the SearchListingView, no authentication token is required and a search parameter must be passed in the request.

## Contribution
Pull requests are and new features suggestions are welcomed.
I also plan on adding more features and API's to this project.