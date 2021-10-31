from db_models.mongo_setup import global_init
from db_models.models.cache_model import Cache
global_init()


def location_index(db_object):
    image_location={}
    location_address={}
    image_location=db_object.image_location
    location_address=image_location["location_address"]
    string_index=''

    if location_address["city"]:

        string_index=image_location["location_category"]+location_address['location_name']+\
                     location_address['city']+location_address['county']\
                 +location_address['state_district']+location_address['state']+location_address['country']

    elif location_address["village"]:
        string_index = image_location["location_category"] + location_address['location_name'] +\
                       location_address['village']+ location_address['county'] \
                       + location_address['state_district'] + location_address['state'] + location_address['country']

    return string_index

