import requests
from environment import API_KEY

def validate_postcode(postcode, country_code):
    address = lookup_postcode(postcode, country_code)

    if address is None:
        print("Postcode does not exist")
        return None

    return address


def calculate_distance(point1, point2):
    url = "https://api.geoapify.com/v1/geometry/operation"

    print('\nPoints:')
    print(point1, point2)

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
