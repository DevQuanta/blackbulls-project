import requests
from environment import API_KEY, LAET_POSTCODE, LAET_COUNTRY_CODE

def validate_postcode(postcode, country_code):
    address = lookup_postcode(postcode, country_code)

    if address is None:
        print("Postcode does not exist")
        return None

    return address


def calculate_distance(delivery_postcode, country_code):

    delivery_details = validate_postcode(delivery_postcode, country_code)
    laet_details = validate_postcode(LAET_POSTCODE, LAET_COUNTRY_CODE)

    point1 = get_lat_long(laet_details)
    point2 = get_lat_long(delivery_details)

    url = "https://api.geoapify.com/v1/geometry/operation"

    request_body = {
        "operation": "distance",
        "point1": {
            "type": "Point",
            "coordinates": [
                point1["lon"],
                point1["lat"]
            ]
        },
        "point2": {
            "type": "Point",
            "coordinates": [
                point2["lon"],
                point2["lat"]
            ]
        },
        "params": {
            "units": "miles"
        }
    }

    response = requests.post(url, json=request_body, params = {
            "apiKey": API_KEY
    })

    response.raise_for_status()

    response = response.json()
    return float(f"{response['data']:.2f}")


def lookup_postcode(postcode, country_code):
    url = "https://api.geoapify.com/v1/postcode/search"

    response = requests.get(url, params = {
        "postcode": postcode,
        "countrycode": country_code.lower(),
        "format": "geojson",
        "apiKey": API_KEY
    })

    response.raise_for_status()

    response = response.json()

    normalise = lambda s: "".join(s.upper().split())

    for result in response.get("features", []):
        if (normalise(result.get("properties", "").get("postcode", ""))) == normalise(postcode) and normalise(result.get("properties").get("country_code")) == normalise(country_code):
            return result

    return None



def get_address(details):
    return details["properties"]["address_line1"]

def get_lat_long(details):
    return {
        'lon': details["properties"]["lon"],
        'lat': details["properties"]["lat"]
    }

