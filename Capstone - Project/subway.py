#!/usr/bin/env python3
# subway.py --- an interactive NYC subway program.
# Usage : subway_original.py - CSCI-132 Project.
# Author : Jose Ortiz & Theodoros Bogiatzis
# Created on : November 5, 2024.
# Description : This program will read a CSV file containing subway data and allow users to query the data. The program will provide information about subway stations, routes, and portals.
#
# *************************************************************


import csv
import math
from collections import defaultdict, namedtuple
from geopy.distance import great_circle
import re
import subprocess
import os

# Define data structures
Portal = namedtuple("Portal", ["station_name", "gps_coordinates", "route_sets"])
SubwayRoute = namedtuple("SubwayRoute", ["route_identifier", "stations"])


def portal_names(row):
    """Generates unique and general names for portals."""
    general_name = f"{row['North South Street']}, {row['East West Street']}, {row['Corner']}"
    gps_coordinates = (float(row['Entrance Latitude']), float(row['Entrance Longitude']))
    return general_name, gps_coordinates


def route_sets(portals, stations):
    """Checks for stations with identical route sets and proximity."""
    connected_stations = set()
    for station1 in stations:
        for station2 in stations:
            if station1 == station2:
                continue
            if (
                    set(station1.route_sets) == set(station2.route_sets)
                    and great_circle(station1.gps_coordinates, station2.gps_coordinates).kilometers <= 0.28
            ):
                connected_stations.add((station1.station_name, station2.station_name))  # Store names instead
    return connected_stations


def haversine(lat1, lon1, lat2, lon2):
    """Calculates the distance between two points using GPS coordinates."""
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371  # Radius of Earth in kilometers
    return c * r


def list_stations(stations, output_file):
    """Lists all station names alphabetically."""
    output = "Subway Stations:\n"
    for station in sorted(stations, key=lambda x: x.station_name):
        output += station.station_name + "\n"
    print(output)
    output_file.write(output)


def list_route_stations(stations, route_identifier, output_file):
    """Lists stations served by a specific route."""
    output = f"Stations on Route {route_identifier}:\n"
    for station in stations:
        if route_identifier in station.route_sets:
            output += station.station_name + "\n"
    print(output)
    output_file.write(output)


def list_routes(portals, portal_name, output_file):
    """Lists routes accessible at a specific portal."""
    output = ""
    for portal in portals:
        if portal.station_name == portal_name:  # Ensure comparison is correct
            output = f"Routes at {portal.station_name}: {', '.join(portal.route_sets)}\n"
            break
    else:
        output = f"No portal found for {portal_name}\n"
    print(output)
    output_file.write(output)


def list_station_portals(portals, station_name, output_file):
    """Lists all portals for a given station and their entrance types."""
    output = f"Portals for Station {station_name}:\n"
    for portal in portals:
        if portal.station_name == station_name:
            output += f"  {portal.station_name} ({portal.route_sets})\n"
    print(output)
    output_file.write(output)


def nearest_portal(portals, latitude, longitude, output_file):
    """Finds the closest portal and its routes."""
    closest_distance = float("inf")
    closest_portal = None
    for portal in portals:
        distance = haversine(latitude, longitude, portal.gps_coordinates[0], portal.gps_coordinates[1])
        if distance < closest_distance:
            closest_distance = distance
            closest_portal = portal
    output = (f"Closest portal: {closest_portal.station_name} ({closest_portal.gps_coordinates})\n"
              f"Closest routes: {', '.join(closest_portal.route_sets)}\n")
    print(output)
    output_file.write(output)


def check_line(line):
    # This function check every value in the line (list) passed as argument to see
    # if it matches the regex pattern specified for that line

    # some of the regex patterns maybe have to be loosened up because they may
    # not match future values if someone edits the file

    # For the given file it works fine and given that the specified
    # format of the file is going to be the same is going to be alright

    # The file is inconsistent at some points as some values maybe
    # have the same meaning with others
    # example: W, West

    text_regex = r"^[a-zA-Z0-9\- :&()'.]+$"
    text_regex_n = r"^[a-zA-Z0-9\- :&()'.]+$|^$"
    float_regex = r"^\-?[0-9]+(\.?[0-9]+)?$"
    route_regex = r"[a-zA-Z0-9]|^$"
    coordinates_regex = r"^\(\-?[0-9]+(\.?[0-9]+)?,\s\-?[0-9]+(\.?[0-9]+)?\)$"

    if not line[0] in ["BMT", "IND", "IRT"]:  # Division
        print("Value: " + line[0] + " in line 0 is invalid")
        return False
    if not re.match(text_regex, line[1]):  # Line
        print("Value: " + line[1] + " in line 1 is invalid")
        return False
    if not re.match(text_regex, line[2]):  # Station Name
        print("Value: " + line[2] + " in line 2 is invalid")
        return False
    if not re.match(float_regex, line[3]):  # Station Latitude
        print("Value: " + line[3] + " in line 3 is invalid")
        return False
    if not re.match(float_regex, line[4]):  # Station Longtitude
        print("Value: " + line[4] + " in line 4 is invalid")
        return False
    if not re.match(route_regex, line[5]):  # Route 1
        print("Value: " + line[5] + " in line 5 is invalid")
        return False
    if not re.match(route_regex, line[6]):  # Route 2
        print("Value: " + line[6] + " in line 6 is invalid")
        return False
    if not re.match(route_regex, line[7]):  # Route 3
        print("Value: " + line[7] + " in line 7 is invalid")
        return False
    if not re.match(route_regex, line[8]):  # Route 4
        print("Value: " + line[8] + " in line 8 is invalid")
        return False
    if not re.match(route_regex, line[9]):  # Route
        print("Value: " + line[9] + " in line 9 is invalid")
        return False
    if not re.match(route_regex, line[10]):  # Route 6
        print("Value: " + line[10] + " in line 10 is invalid")
        return False
    if not re.match(route_regex, line[11]):  # Route 7
        print("Value: " + line[11] + " in line 11 is invalid")
        return False
    if not re.match(route_regex, line[12]):  # Route 8
        print("Value: " + line[12] + " in line 12 is invalid")
        return False
    if not re.match(route_regex, line[13]):  # Route 9
        print("Value: " + line[13] + " in line 13 is invalid")
        return False
    if not re.match(route_regex, line[14]):  # Route 10
        print("Value: " + line[14] + " in line 14 is invalid")
        return False
    if not re.match(route_regex, line[15]):  # Route 11
        print("Value: " + line[15] + " in line 15 is invalid")
        return False
    if not line[16] in ["Stair", "Escalator", "Elevator", "Easement", "Door", "Ramp", "Walkway"]:  # Entrance Type
        print("Value: " + line[16] + " in line 16 is invalid")
        return False
    if not line[17] in ["YES", "NO"]:  # Entry
        print("Value: " + line[17] + " in line 17 is invalid")
        return False
    if not line[18] in ["Yes", ""]:  # Exit only
        "Value: " + line[18] + " in line 18 is invalid"
        return False
    if not line[19] in ["YES", "NO"]:  # Vending
        "Value: " + line[19] + " in line 19 is invalid"
        return False
    if not line[20] in ["FULL", "NONE", "PART", "Spc Ev"]:  # Staffing
        "Value: " + line[20] + " in line 20 is invalid"
        return False
    if not re.match(text_regex_n, line[21]):  # Staff Hours
        print("Value: " + line[21] + " in line 21 is invalid")
        return False
    if not line[22] in ["TRUE", "FALSE"]:  # ADA
        "Value: " + line[22] + " in line 22 is invalid"
        return False
    if not re.match(text_regex_n, line[23]):  # ADA NOTES
        "Value: " + line[23] + " in line 23 is invalid"
        return False
    if line[24] not in ["TRUE", "FALSE"]:  # Free crossover
        print("Value: " + line[24] + " in line 24 is invalid")
        return False
    if not re.match(text_regex_n, line[25]):  # North South Street
        print("Value: " + line[25] + " in line 25 is invalid")
        return False
    if not re.match(text_regex_n, line[26]):  # East West Street
        print("Value: " + line[26] + " in line 26 is invalid")
        return False
    if not line[27] in ["NW", "NE", "SE", "SW", "W", "N", "E", "S", "West", ""]:  # Corner
        print("Value: " + line[27] + " in line 27 is invalid")
        return False
    if not re.match(float_regex, line[28]):  # Entrance Latidude
        print("Value: " + line[28] + " in line 28 is invalid")
        return False
    if not re.match(float_regex, line[29]):  # Entrace Longtitude
        print("Value: " + line[29] + " in line 29 is invalid")
        return False
    if not re.match(coordinates_regex, line[30]):  # Station Location
        print("Value: " + line[30] + " in line 30 is invalid")
        return False
    if not re.match(coordinates_regex, line[31]):  # Entrance Location
        print("Value: " + line[31] + " in line 31 is invalid")
        return False
    return True


def check_file_lines(csv_filename):
    # This function makes some initial checks to the file, checking at first that the header is right
    # and then checks if each line has the right length and passes the line to check_line function to
    # see if each value of the line matches the regex

    with open(csv_filename) as f:
        reader = csv.reader(f)
        data = list(reader)
        if (data[0] != ['Division', 'Line', 'Station Name', 'Station Latitude', 'Station Longitude', 'Route1', 'Route2',
                        'Route3', 'Route4', 'Route5', 'Route6', 'Route7', 'Route8', 'Route9', 'Route10', 'Route11',
                        'Entrance Type',
                        'Entry', 'Exit Only', 'Vending', 'Staffing', 'Staff Hours', 'ADA', 'ADA Notes',
                        'Free Crossover', 'North South Street',
                        'East West Street', 'Corner', 'Entrance Latitude', 'Entrance Longitude', 'Station Location',
                        'Entrance Location']):
            print("Invalid file format: Header")  # Check header
            return False
        for line in data[1:-1]:  # Exclude the header
            if len(line) != 32:  # Check line length
                print("Invalid file format: Line length")
                return False
            if not check_line(line):  # check if all the values of the line match the regex
                return False
        return True


def getUsername():
    try:
        username = subprocess.run("echo %USERNAME%", capture_output=True, text=True, shell=True).stdout.split("\n")[0]
        return username
    except:
        username = ""


def main():
    user = getUsername()
    try:
        data_file = 'C:/Users/' + user + '/Desktop/nyc_subway_stations.csv'
        if not os.path.exists(data_file):
            raise ("file not found")
        # Open the output file for writing
        output_file = open('C:/Users/' + user + '/Desktop/subway_output.txt', 'w')
    except:
        try:
            data_file = 'C:/Users/' + user + '/OneDrive/Desktop/nyc_subway_stations.csv'
            # Open the output file for writing
            if not os.path.exists(data_file):
                raise ("file not found")
            output_file = open('C:/Users/' + user + '/OneDrive/Desktop/subway_output.txt', 'w')
        except:
            try:
                data_file = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop/nyc_subway_stations.csv')
                # Open the output file for writing
                if not os.path.exists(data_file):
                    raise ("file not found")
                output_file = open(os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop/subway_output.txt'),
                                   'w')
            except:
                try:
                    data_file = "./nyc_subway_stations.csv"
                    if not os.path.exists(data_file):
                        raise ("file not found")
                    output_file = open('./subway_output.txt', 'w')
                except:
                    print(
                        "Add files nyc_subway_stations.csv and subway_output.txt to Desktop or current working folder")
                    exit()

    portals = []
    station_list = []
    route_sets_map = defaultdict(set)

    with open(data_file, "r") as f:
        if not check_file_lines(data_file):  # check the file
            exit(-1)  # if file is invalid exit with code -1
        reader = csv.DictReader(f)
        for row in reader:
            general_name, gps_coordinates = portal_names(row)

            # Create a set of routes from the Route columns
            route_columns = ["Route1", "Route2", "Route3", "Route4", "Route5", "Route6",
                             "Route7", "Route8", "Route9", "Route10", "Route11"]
            route_set = set(row[route] for route in route_columns if row[route])  # Renamed this variable

            portal = Portal(row["Station Name"], gps_coordinates, route_set)
            portals.append(portal)
            station_list.append(portal)
            route_sets_map[portal.station_name].update(route_set)

    connected_stations = route_sets(portals, station_list)  # This should now work without conflict

    while True:
        command = input(
            "Enter a command (liststations, listroutestations, listroutes, liststationportals, nearest, help, quit): ")

        if command == "liststations":
            list_stations(station_list, output_file)
        elif command == "listroutestations":
            route_identifier = input("Enter route identifier: ")
            list_route_stations(station_list, route_identifier, output_file)
        elif command == "listroutes":
            portal_name = input("Enter portal name or GPS coordinates: ")
            list_routes(portals, portal_name, output_file)
        elif command == "liststationportals":
            station_name = input("Enter station name: ")
            list_station_portals(portals, station_name, output_file)
        elif command == "nearest":
            latitude = float(input("Enter latitude: "))
            longitude = float(input("Enter longitude: "))
            nearest_portal(portals, latitude, longitude, output_file)
        elif command == "help":
            help_text = ("Available commands:\n"
                         "  liststations: List all stations\n"
                         "  listroutestations <route_identifier>: List stations on a route\n"
                         "  listroutes <portal_name>: List routes at a portal\n"
                         "  liststationportals <station_name>: List portals for a station\n"
                         "  nearest <latitude> <longitude>: Find the nearest portal\n"
                         "  help: Display this help message\n"
                         "  quit: Exit the program")
            print(help_text)
            output_file.write(help_text + "\n")
        elif command == "quit":
            break
        else:
            error_message = "Invalid command. Type 'help' for the list of valid commands.\n"
            print(error_message)
            output_file.write(error_message)

    # Close the output file when done
    output_file.close()


if __name__ == "__main__":
    main()