from . models import Listing

def delete_realtors_listing(realtor_email):
    if Listing.objects.filter(realtor=realtor_email).exists():
        Listing.objects.filter(realtor=realtor_email).delete()