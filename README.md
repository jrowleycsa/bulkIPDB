# bulkIPDB

bulkIPDB is a Python script designed to fetch detailed information about IP addresses from the AbuseIPDB API and IP2Location database. It can process multiple IP addresses stored in a CSV file and outputs the results to both a CSV file and a text file.

## Prerequisites
- Python 3.x installed
- requests (pip install requests)
- IP2Location (pip install IP2Location)

## Setup

1. Clone the repository: `git clone https://github.com/jrowleycsa/ip-info-checker.git`
2. Obtain an API key from [abuseIPDB](https://www.abuseipdb.com)
3. Download the IP2Location database file from [IP2Location Lite](https://lite.ip2location.com/ip2location-lite)
4. Add your AbuseIPDB API key to a file named api.txt and add its path within the script (/path/to/api.txt).
5. Ensure you have the IP2Location database file (IP2LOCATION-LITE-DB5.IPV6.BIN) and add its path within the script (/path/to/IP2LOCATION-LITE-DB5.IPV6.BIN).
6. Create a CSV file in the location set within the script. The name of this file will be passed into the script as an argument and the file will be used to input the IPs to be queried into the script.

## Usage
1. Add the IPs to request, as rows within the first column of the CSV file created above.
   
   ![image](https://github.com/jrowleycsa/bulkIPDB/assets/152403367/d5690e88-184c-4b56-b3d6-f443b5787a86)
3. Run the script with the CSV input file as an argument ie: `python bulkIPDB.py ipInput.csv`
4. The script will process each IP address in the CSV file, fetch abuse reports and geolocation information, and output the results to ipResults.csv and ipResults.txt.
   
![image](https://github.com/jrowleycsa/bulkIPDB/assets/152403367/66a5a167-5085-4722-98c0-d9c0c6913e9a)

## Examples
### IP result to CSV
![image](https://github.com/jrowleycsa/bulkIPDB/assets/152403367/dc7f1b06-7978-4038-aa29-5ce1466e531c)

### IP result to TXT
![image](https://github.com/jrowleycsa/bulkIPDB/assets/152403367/4fcef3b9-4400-4509-aa6b-e3018cda476f)



    
