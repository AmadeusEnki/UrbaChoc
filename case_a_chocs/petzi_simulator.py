# Description: This script simulates a petzi webhook request.
#   ____                    _       ____ _
#  / ___|__ _ ___  ___     / \     / ___| |__   ___   ___ ___
# | |   / _` / __|/ _ \   / _ \   | |   | '_ \ / _ \ / __/ __|
# | |__| (_| \__ \  __/  / ___ \  | |___| | | | (_) | (__\__ \
#  \____\__,_|___/\___| /_/   \_\  \____|_| |_|\___/ \___|___/

import argparse
import datetime
import hmac

import requests


def make_header(body, secret):
    unix_timestamp = str(datetime.datetime.timestamp(datetime.datetime.now())).split('.')[0]
    body_to_sign = f'{unix_timestamp}.{body}'.encode()
    digest = hmac.new(secret.encode(), body_to_sign, "sha256").hexdigest()
    # Set the headers for the POST request
    headers = {'Petzi-Signature': f't={unix_timestamp},v1={digest}', 'Petzi-Version': '2',
               'Content-Type': 'application/json', 'User-Agent': 'PETZI webhook'}
    return headers


def make_post_request(url, data, secret):
    try:
        # Make the POST request
        response = requests.post(url, data=data, headers=make_header(data, secret))

        if response.status_code == 200:
            print(f"Request successful. Response: {response.text}")
        else:
            print(f"Request failed with status code {response.status_code}.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    # Create a command line argument parser
    parser = argparse.ArgumentParser(description="HTTP POST Request with JSON Body")
    parser.add_argument("url", type=str, help="URL to send the POST request to")
    parser.add_argument("secret", nargs='?', type=str, help="secret shared between your server and petzi simulator",
                        default="secret")

    # Parse the command line arguments
    args = parser.parse_args()

    # Coding horror : Don't Do This at Home!
    data = '''{
           "event":"ticket_created",
           "details":{
              "ticket":{
                 "number":"wgiubwfwdewgrgwfefbffz3",
                 "type":"online_presale",
                 "title":"My Parent Ticket",
                 "category":"My Categoryyy23512367721223211232323233",
                 "eventId":12345,
                 "event":"Helq112l2o",
                 "cancellationReason":"",
                 "sessions":[
                    {
                       "name":"Session name",
                       "date":"2023-04-28",
                       "time":"19:00:00",
                       "doors":"20:00:00",
                       "location":{
                          "name":"location",
                          "street":"2960 Curtis Course Suite 823",
                          "city":"East Monicaborough",
                          "postcode":"84458"
                       }
                    }
                 ],
                 "promoter":"Member namse",
                 "price":{
                    "amount":"100.00",
                    "currency":"CHF"
                 }
              },
              "buyer":{
                 "role":"customer",
                 "firstName":"Janeea bddilly",
                 "lastName":"Doe deq",
                 "postcode":"1234"
              }
           }
        }'''

    # Make the POST request
    make_post_request(args.url, data, args.secret)
