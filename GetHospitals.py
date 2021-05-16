import requests
import urllib.parse
import json
import pandas as pd

class GetHospitals:

    bingMapsKey = "AjZ6iZB1unxRzkQzJEz5uJMQVWPT5LYbrQIkvyytwlmFwxWc3Xj8D9jgNQFMV0XR"
    outp = {}
    
    def calculateCordinates(self,addr):
        encodeaddr = urllib.parse.quote(addr, safe='')
        url = 'http://dev.virtualearth.net/REST/v1/Locations?q='+encodeaddr+'&key='+self.bingMapsKey 
        response = requests.get(url).json()
        result = response
        cord = result["resourceSets"][0]["resources"][0]["point"]["coordinates"]
        return cord

    def calculateDistanceTime(self,srcll,destll):
        payload = {
		    "origins": srcll,
		    "destinations": destll,
		    "travelMode": "driving",
		}

        paramtr = {"key": self.bingMapsKey}

        res = requests.post('https://dev.virtualearth.net/REST/v1/Routes/DistanceMatrix',data = 
		json.dumps(payload), params = paramtr)

        result = res.json()
        return result["resourceSets"][0]["resources"][0]["results"]

    def getHospitalsList(self,lat,lon,disease):
        data = pd.read_csv('Hospital_Information.csv')
        index = data[data['Disease Name'] != disease].index
        data.drop(index,inplace = True)
        data['mean'] = data.iloc[:,-6:-1].mean(axis = 1)
        review = data.groupby('Hospital Name')['mean'].mean().to_frame(name = 'mean').reset_index()
        count = data['Hospital Name'].value_counts().to_frame(name = 'count').reset_index()
        count.rename(columns = {'index': 'Hospital Name'}, inplace = True)
        rcmerge = pd.merge(review,count) # r = review, c = count  
        hgb = data.iloc[:,[1,3,5]] #h = Hospital Name, g = Hospital Address/google address, b = Bing Address
        hgb = hgb.groupby(['Hospital Name']).agg(lambda x: ''.join(set(x))).reset_index()
        data = pd.merge(rcmerge,hgb)
        dest = data.iloc[:,4].values
        srclatlong = [{"latitude": lat, "longitude": lon}]
        destlatlong = []
        for i in range(0,len(dest)):
            cord = self.calculateCordinates(dest[i])
            destlatlong.append({"latitude": cord[0], "longitude": cord[1]})
        distTime = self.calculateDistanceTime(srclatlong,destlatlong);
        distdict = {}
        for i in range(0,len(distTime)):
            distdict[dest[i]] = distTime[i]['travelDistance']
        distdict = sorted(distdict.items(), key=lambda x: x[1])
        distdata = pd.DataFrame(distdict)
        distdata.rename(columns = {0: 'Bing Address',1: 'Distance'}, inplace = True)
        data = pd.merge(data,distdata)
        data.drop(['Bing Address'],axis=1,inplace = True)
        data.sort_values(by=['Distance'], inplace=True)
        arr = data.values
        self.outp.clear();
        for i in range(0,len(arr)):
        	self.outp[arr[i][0]] = {}
        	self.outp[arr[i][0]]['review'] = str(arr[i][1])
        	self.outp[arr[i][0]]['count'] = str(arr[i][2])
        	self.outp[arr[i][0]]['address'] = str(arr[i][3])
        	self.outp[arr[i][0]]['distance'] = str(arr[i][4])

#obj = GetHospitals()
#obj.getHospitalsList(20,78,'Acne')
#print(obj.outp)
