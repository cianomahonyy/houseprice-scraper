from bs4 import BeautifulSoup
import requests
import matplotlib.pyplot as plt
import pandas as pd

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.90 Safari/537.36'}

listOfPrices = []
xPlot = []
listOfAverages = []

count = 20

pandaListOfCounties = []
pandaListOfPrices = []
listOfHouseTypes = []
listOfAddresses = []

listOfCounties = ['carlow', 'cavan', 'clare', 'cork', 'donegal', 'dublin', 'galway', 'kerry', 'kildare', 'kilkenny', 'laois', 'leitrim', 'limerick', 'louth', 'mayo', 'meath', 'offaly', 'roscommon', 'sligo', 'tipperary', 'waterford', 'westmeath', 'wexford', 'wicklow']

def getAverage(listOfPrices):
	averagePrice = sum(listOfPrices) / float(len(listOfPrices))
	averagePrice = round(averagePrice)
	return averagePrice

for place in listOfCounties:

	listOfPrices = []

	for i in range(0,500):	

		url = 'https://www.daft.ie/' + place + '/houses-for-sale/?offset='
		url = url + str(count)
		count = count + 20

		response = requests.get(url, headers=headers)
		c = response.content

		soup = BeautifulSoup(c, features='html.parser')

		prices = soup.find_all('strong', 'PropertyInformationCommonStyles__costAmountCopy')
		houseTypes = soup.find_all('div', {'class': 'QuickPropertyDetails__propertyType'})
		houseAddress = soup.find_all('a', 'PropertyInformationCommonStyles__addressCopy--link')

		for price, house, address in zip(prices, houseTypes, houseAddress):
			itemPrice = price.get_text()
			itemPrice = itemPrice.replace("€","")
			itemPrice = itemPrice.replace(",","")
			if(itemPrice.isdigit()):
				itemPrice = int(itemPrice)
				listOfPrices.append(itemPrice)
				pandaListOfCounties.append(place)
				pandaListOfPrices.append(itemPrice)
				newHouse = house.get_text()
				newAddress = address.get_text()
				listOfHouseTypes.append(newHouse)
				listOfAddresses.append(newAddress)
				print(newAddress)

		if(prices == []):
			break

		print(listOfPrices)
		print(url)
	
	averageStatement = 'The average price of a house in ' + place + ' is €' + str(getAverage(listOfPrices))
	averageHousePrice = getAverage(listOfPrices)

	listOfAverages.append(averageHousePrice)

	count = 0


house_details = {
	'county':pandaListOfCounties,
	'price':pandaListOfPrices,
	'house_type':listOfHouseTypes,
	'house_address':listOfAddresses
}

df = pd.DataFrame(house_details)
print(df.head(50))
df.to_csv('county_prices.csv', index=True, encoding='utf-8')


plt.barh(listOfCounties, listOfAverages)
plt.xlabel('Counties')
plt.ylabel('Average Price')
plt.title('Average Prices')
plt.legend()
plt.show()







