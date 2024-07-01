#!/usr/bin/python3
"""
Set up a basic web server in your preferred stack.
Deploy it to any free hosting platform and expose an
API endpoint that conforms to the criteria below:
    Endpoint: [GET] <example.com>/api/hello?visitor_name="Mark"
    (where <example.com> is your server origin)
"""


import requests
from flask import request, jsonify, abort
from app import app
from datetime import datetime
from collections import OrderedDict


def get_visitor_ip():
    """
    Get the real IP of the visitor
    in the case of a reverse proxy or load balancer
    """
    ip = request.headers.get('X-Forwarded-For', None)
    if ip:
        ip = ip.split(',')[0]
        return ip
    else:
        return request.remote_addr


def get_ip_location(ip):
    """
    Get the location of the IP address
    """
    location = []
    ip = "191.96.227.23"
    url = f'http://ip-api.com/json/{ip}'
    response = requests.get(url).json()
    if response.get('status') == 'success':
        location.append(response['city'])
        location.append(response['lat'])
        location.append(response['lon'])
    return location


def get_temperature(location):
    """
    Get the temperature of visitor location
    """
    lat = location[1]
    lon = location[2]
    current_date = datetime.now().strftime('%Y-%m-%d')
    url = f'https://api.brightsky.dev/weather?lat={lat}&lon={lon}&date={current_date}'
    response = requests.get(url).json()
    temperature = response['weather'][0]['temperature']
    return temperature


@app.route('/', methods=['GET'], strict_slashes=False)
def home():
    """
    Homepage
    """
    return ('<h1> Hello World!</h1>')


@app.route('/api/hello', methods=['GET'])
def hello():
    """
    Create a JSON response that includes the
    client IP, location, and greeting with the temperature.
    """
    visitor_name = request.args.get('visitor_name', 'Stranger')
    visitor_ip = get_visitor_ip()

    ip_location = get_ip_location(visitor_ip)
    temperature = get_temperature(ip_location)

    response = {
            "client_ip": visitor_ip,
            "location": ip_location[0],
            "greeting": f'Hello, {visitor_name}!, the temperature is {temperature} degrees Celcius in {ip_location[0]}'
         }

    return jsonify(response), 200
