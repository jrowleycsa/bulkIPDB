import requests
import json
import csv
from sys import argv
import IP2Location
import os

# Setting API key
apiFile = "/path/to/api.txt"

# Predetermined path to CSV file with IPs to check, the file name is a command line argument.
ipFile = "/path/to/"+argv[1]

# Path and file name for the results file
csvRes = "ipResults.csv"
txtRes = "ipResults.txt"

# Connecting to IP2Location DB
dbpath = "/path/to/IP2LOCATION-LITE-DB5.IPV6.BIN"  # Path to the database file
dbconn = IP2Location.IP2Location(os.path.join("data", dbpath))

# Reading API key
with open(apiFile, "r") as apiF:
    api = apiF.read()

# Opening CSV for read and write, looping through the IP addresses in the source file.
with open(ipFile, 'r') as ipF, open(csvRes, "w", newline='') as resF, open(txtRes, "w") as txtF:
    ips = csv.reader(ipF)
    next(ips, None)  # skipping header

    # Setting csv writer
    writer = csv.writer(resF)

    # Setting header row for results file
    writer.writerow(["IPAddress", "ISP", "City Name", "Region", "CountryName", "TotalReports", "AbuseConfidence", "Usage", "CountryCode", "Public"])

    num_ips_found = 0
    total_ips = len(list(ips))  # Count total IPs in the CSV

    for ip in csv.reader(open(ipFile)):
        if not ip:
            continue
        else:
            # API url to check the IPs
            url = 'https://api.abuseipdb.com/api/v2/check'

            # Query
            querystring = {
                'ipAddress': ip,
                'maxAgeInDays': '365',
                'verbose': ''
            }

            headers = {
                'Accept': 'application/json',
                'Key': api
            }

            try:
                response = requests.request(method='GET', url=url, headers=headers, params=querystring, timeout=60)
                response.raise_for_status()

                # Check if 'response' is defined
                if response is not None:
                    try:
                        # Parse the JSON response
                        results = json.loads(response.text)
                        # Continue processing the results

                        # Increment the count of IPs found
                        num_ips_found += 1

                        # Print to terminal when a new IP is found
                        print(f"IP {num_ips_found}/{total_ips} found: {ip[0]}")

                        # Getting DB results for IP address
                        ip2loc = dbconn.get_all(ip[0])

                        # Results in json format
                        results = json.loads(response.text)

                        # Checking if key exists as countryName and City key is missing
                        if "ipAddress" in results['data']:
                            ipaddr = str(results['data']['ipAddress'])
                        else:
                            ipaddr = "NaN"

                        if "isPublic" in results['data']:
                            isPub = str(results['data']['isPublic'])
                        else:
                            isPub = "NaN"

                        if "isp" in results['data']:
                            isp = str(results['data']['isp'])
                        else:
                            isp = "NaN"

                        if ip2loc.city:
                            cityName = str(ip2loc.city)
                        else:
                            cityName = "NaN"

                        if ip2loc.region:
                            regionName = str(ip2loc.region)
                        else:
                            regionName = "NaN"

                        if "countryName" in results['data']:
                            countryName = str(results['data']['countryName'])
                        else:
                            countryName = "NaN"

                        if "countryCode" in results['data']:
                            countryCode = str(results['data']['countryCode'])
                        else:
                            countryCode = "NaN"

                        if "totalReports" in results['data']:
                            totalRep = str(results['data']['totalReports'])
                        else:
                            totalRep = "NaN"

                        if "abuseConfidenceScore" in results['data']:
                            abuseConf = str(results['data']['abuseConfidenceScore'])
                        else:
                            abuseConf = "NaN"

                        if "usageType" in results['data']:
                            usageType = str(results['data']['usageType'])
                        else:
                            usageType = "NaN"

                        # Writing to the results csv file.
                        writer.writerow([ipaddr, "owned by " + isp, "and hosted in " + cityName + ",", regionName + ",",
                                         countryName + ",", "with " + totalRep + " reports of abuse ",
                                         "and an abuse confidence rate of " + abuseConf + "%", usageType, countryCode, isPub])

                        # Writing to the results text file.
                        txtF.write(f"- '{ipaddr}' owned by '{isp}' and hosted in {cityName}, {regionName},"
                                    f"{countryName}, with {totalRep} reports of abuse,"
                                    f"and an abuse confidence rate of {abuseConf}%\n")

                    except json.JSONDecodeError as json_error:
                        # Handle JSON decoding errors
                        print(f"JSON Decode Error: {json_error}")
            except requests.exceptions.RequestException as e:
                # Handle request exceptions (e.g., timeouts, connection errors)
                print(f"Error: {e}")
                response = None  # Set response to None in case of an exception

                # Write an error entry to the CSV file
                writer.writerow(["Error", f"Error fetching data for IP: {str(ip)}"])
                print(f"Error fetching data for IP: {str(ip)}")

    # Print a message indicating that the data has been written to the CSV file
    print(f"Data has been written to {csvRes} and {txtRes}.")
