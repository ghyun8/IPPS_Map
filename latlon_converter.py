import csv
import googlemaps
from googlemaps import client

# API = 'AIzaSyC1vrBspDxhJrc4U2vEoDDgceosKp3_Dz8'
API = 'AIzaSyC0K-YdtaagBKb8S0egi4hTrn5xheYvwqw'
# API = 'AIzaSyAvvjBBleVflH_KXaAhWu4cupZsj2DtX04'
# API = 'AIzaSyCuI5pO-R6Pl_LMORS63U3pd-USnhloQpw'

client = googlemaps.Client(key=API)
filename = 'Data/data8' #input filename (e.g. Data\...)
new_filename= 'Data/data8latlon'

address = [] # List of address of provider
coordinates = [['Latitude','Longtitude']] # List of coordniates
new_rows = [] # To rewrite over the CVS file

with open (filename) as csvfile:
	reader=csv.DictReader(csvfile)
	for row in reader:
		# address = row.get('Provider State'),row.get('Provider Zip Code')
		one_address = row['Provider Street Address'] + " " + row['Provider City'] + " " + row['Provider State']
		address.append(one_address)

def address_to_latlon(client,address):
	"""converts address to latitude and longtitude"""
	params = {}

	if address:
	    params["address"] = address

	latlon_raw = client._get("/maps/api/geocode/json", params)["results"]
	for dictionary in latlon_raw:
		location = dictionary.get('geometry')
		break
	latlon = location.get ('location')
	return [latlon.get('lat'), latlon.get('lng')]

# print addresstolatlon(client,address)

for each_address in address:
	print each_address
	coordinates.append(address_to_latlon(client, each_address))

"""adding latitude and longtitude to CSV file"""

with open (filename,'rb') as csvfile:
	reader=csv.reader(csvfile)
	for i,row in enumerate(reader):
		new_row=row
		new_row.append(coordinates[i][0])
		new_row.append(coordinates[i][1])
		new_rows.append(new_row)

with open (new_filename,'wb') as csvfile:
	writer=csv.writer(csvfile)
	writer.writerows(new_rows)
