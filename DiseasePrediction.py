import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

class DiseasePrediction:
	rfc = ""
	x_test = ""
	y_test = ""
	datacols = ""
	
	def CalculateRFC(self,file_name):
		dataset = pd.read_csv(file_name)
		cols = [i for i in dataset.iloc[:,1:].columns]
		temp = pd.melt(dataset.reset_index(),id_vars = ['index'], value_vars = cols )
		temp['status'] = 1
		data = pd.pivot_table(temp,values = 'status',index = 'index',columns = 'value')
		data.rename(columns=lambda x: x.strip(), inplace=True)
		self.datacols = list(data.columns)
		data.insert(0,'Disease',dataset['Disease'])
		data = data.fillna(0) 

		x = data.iloc[:,1:]
		y = data.iloc[:,0]

		x_train, self.x_test, y_train, self.y_test = train_test_split(x, y, test_size = 0.3, random_state = 0)
		self.rfc = RandomForestClassifier(n_estimators=100,random_state = 0)
		self.rfc.fit(x_train, y_train)
		
	def accuracyScore(self):
		y_pred = self.rfc.predict(self.x_test)
		a = accuracy_score(self.y_test,y_pred)
		print("The accuracy of this model is: ", a*100)

