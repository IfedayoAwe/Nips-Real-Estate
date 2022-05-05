from functools import partial
from rest_framework.views import APIView
from rest_framework.response import Response
from . models import Listing
from rest_framework import status, permissions
from . serializers import ListingSerializer


class ManageListingView(APIView):
    def get(self, request, format=None):
        try:   
            user = request.user
            if not user.is_realtor:
                return Response(
                    {"error": "Normal users don't have listings"},
                    status = status.HTTP_403_FORBIDDEN
                )

            slug = request.query_params.get('slug')
            if not slug:
                listing = Listing.objects.filter(
                    realtor = user.email
                ).order_by('-date_created')
                listing = ListingSerializer(listing, many=True)
                return Response(
                    {"listings": listing.data},
                    status = status.HTTP_200_OK
                )

            if not Listing.objects.filter(
                realtor = user.email,
                slug=slug
            ).exists():
                return Response(
                    {"error": "Listing does not exists"},
                    status = status.HTTP_404_NOT_FOUND
                )

            listing = Listing.objects.get(realtor=user.email, slug=slug)
            listing = ListingSerializer(listing)
            return Response(
                {"listing": listing.data},
                status = status.HTTP_200_OK
            )

        except:
            return Response(
                {"error": "Something went wrong when retrieving listings."},
                status = status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def validate_data(self, data):

            title = data['title']
            address = data['address']
            city = data['city']
            state = data['state']
            zipcode = data['zipcode']
            slug = data['slug']
            description = data['description']

            try:
                price = int(data['price'])
                bedrooms = int(data['bedrooms'])
            except:
                return Response(
                    {"error": "Must be an Integer."},
                    status = status.HTTP_400_BAD_REQUEST
                )

            try:
                bathrooms = float(data['bathrooms'])
            except:
                return Response(
                    {"error": "Bedrooms must be a float value."},
                    status = status.HTTP_400_BAD_REQUEST
                )
            if bathrooms <= 0 or bathrooms >= 10:
                bathrooms = 1.0
            bathrooms = round(bathrooms, 1)
 
            sale_type = data['sale_type']
            if sale_type == "FOR_RENT":
                sale_type = 'For Rent'
            else:
                sale_type = 'For Sale'

            home_type = data['home_type']
            if home_type == "CONDO":
                home_type = 'Condo'
            elif home_type == 'TOWNHOUSE':
                home_type = 'Townhouse'
            else:
                home_type = 'House'

            main_photo = data['main_photo']
            photo_1 = data['photo_1']
            photo_2 = data['photo_2']
            photo_3 = data['photo_3']

            is_published = data['is_published']
            if is_published == "True":
                is_published = True
            else:
                is_published = "False"

            data = {
                'title': title,
                'address': address,
                'city': city,
                'state': state,
                'zipcode': zipcode,
                'description': description,
                'price': price,
                'bedrooms': bedrooms,
                'bathrooms': bathrooms ,
                'sale_type': sale_type ,
                'home_type': home_type ,
                'main_photo': main_photo ,
                'photo_1': photo_1,
                'photo_2': photo_2 ,
                'photo_3': photo_3 ,
                'is_published': is_published,
                'slug': slug
            }
            return data
            
    def post(self, request, format=None):
        try:
            user = request.user
            if not user.is_realtor:
                return Response(
                    {"error": "Only realtors can create listings"},
                    status = status.HTTP_403_FORBIDDEN
                )

            data = request.data
            data = self.validate_data(data)

            title = data['title']
            address = data['address']
            city = data['city']
            state = data['state']
            zipcode = data['zipcode']
            description = data['description']
            price = data['price']
            bedrooms = data['bedrooms']
            bathrooms = data['bathrooms'] 
            sale_type = data['sale_type']
            home_type = data['home_type']
            main_photo = data['main_photo']
            photo_1 = data['photo_1']
            photo_2 = data['photo_2']
            photo_3 = data['photo_3'] 
            is_published = data['is_published']

            slug = data['slug']
            if Listing.objects.filter(slug=slug).exists():
                return Response(
                    {"slug": "Listing with this slug already exists."},
                    status = status.HTTP_400_BAD_REQUEST
                )
            
            Listing.objects.create(
                realtor = user.email,
                title = title,
                slug = slug,
                address = address,
                city = city,
                state = state,
                zipcode = zipcode,
                description = description,
                price = price,
                bedrooms = bedrooms,
                bathrooms = bathrooms ,
                sale_type = sale_type ,
                home_type = home_type ,
                main_photo = main_photo ,
                photo_1 = photo_1,
                photo_2 = photo_2 ,
                photo_3 = photo_3 ,
                is_published = is_published,
            )

            return Response(
                {"success": "Listing created sucessfully."},
                status = status.HTTP_201_CREATED
            )
        except:
            return Response(
                {"error": "Something went wrong when creating listing"},
                status = status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def put(self, request, pk, format=None):
        try:

            try:
                listing = Listing.objects.get(pk=pk)
            except Listing.DoesNotExist:
                return Response(
                    {"error": "Listing does not exist"},
                    status = status.HTTP_404_NOT_FOUND
                )

            user = request.user
            if listing.realtor != user.email:
                return Response({'response': "You don't have permissions to edit that!"})

            data = request.data
            data = self.validate_data(data)

            title = data['title']
            address = data['address']
            city = data['city']
            state = data['state']
            zipcode = data['zipcode']
            description = data['description']
            price = data['price']
            bedrooms = data['bedrooms']
            bathrooms = data['bathrooms'] 
            sale_type = data['sale_type']
            home_type = data['home_type']
            main_photo = data['main_photo']
            photo_1 = data['photo_1']
            photo_2 = data['photo_2']
            photo_3 = data['photo_3'] 
            is_published = data['is_published']

            slug = data['slug']
            if Listing.objects.filter(slug=slug).exists():
                if slug != listing.slug:
                    return Response(
                        {"slug": "Listing with this slug already exists."},
                        status = status.HTTP_400_BAD_REQUEST
                    )

            Listing.objects.filter(realtor=user.email, pk=pk).update(
                title = title,
                slug = slug,
                address = address,
                city = city,
                state = state,
                zipcode = zipcode,
                description = description,
                price = price,
                bedrooms = bedrooms,
                bathrooms = bathrooms ,
                sale_type = sale_type ,
                home_type = home_type ,
                main_photo = main_photo ,
                photo_1 = photo_1,
                photo_2 = photo_2 ,
                photo_3 = photo_3 ,
                is_published = is_published,
            )

            return Response(
                {"success": "Listing sucessfully updated"},
                status = status.HTTP_200_OK
            )

        except:
            return Response(
                {"error": "Something went wrong when updating listing"},
                status = status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ListingDetailView(APIView):
    def get(self, request, format=None):
        try:
            slug = request.query_params.get('slug')
            if not slug:
                return Response(
                    {"error": "Must provide slug"},
                    status= status.HTTP_400_BAD_REQUEST
                )

            if not Listing.objects.filter(slug=slug, is_published=True).exists():
                return Response(
                    {"error": "Published listing with this slug does not exist"},
                    status= status.HTTP_400_BAD_REQUEST
                )

            listing = Listing.objects.get(slug=slug, is_published=True)
            listing = ListingSerializer(listing)
            return Response(
                {"listing":  listing.data},
                status = status.HTTP_200_OK
            )

        except:
            return Response(
                {"error": "Error when retrieving listing detail"},
                status= status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ListingsView(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request, format=None):
            try:
                if not Listing.objects.filter(is_published=True).exists():
                    return Response(
                        {"error": "No published listings available"},
                        status = status.HTTP_404_NOT_FOUND
                    )

                listings = Listing.objects.filter(is_published=True).order_by('-date_created')
                listings = ListingSerializer(listings, many=True)
                return Response(
                    {"listings": listings.data},
                    status = status.HTTP_200_OK
                )

            except: 
                return Response(
                    {"error": "Error when retrieving listing"},
                    status= status.HTTP_500_INTERNAL_SERVER_ERROR
                )