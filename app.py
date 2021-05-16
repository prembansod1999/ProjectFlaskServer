import json
import numpy as np
from flask import Flask, request
from DiseasePrediction import DiseasePrediction
from GetHospitals import GetHospitals
 
app = Flask(__name__)
obj = DiseasePrediction()
obj.CalculateRFC('dataset.csv')
size = len(obj.datacols)

@app.route('/predictDisease',methods=["POST"])
def predict():
    symptoms = request.get_json()
    loc = symptoms.pop(-1)
    latlong = loc.split(' ')
    sympt = []
    sympt = [0 for i in range(size)]    
    for i in symptoms:
        sympt[obj.datacols.index(i)] = 1
    
    disease = str(obj.rfc.predict([sympt])[0])
    print(disease)
    obj2 = GetHospitals()
    obj2.getHospitalsList(latlong[0],latlong[1],disease)
    return json.dumps(obj2.outp)


@app.route('/getHospitals',methods=["POST"])
def predict2():
    info = request.get_json()
    obj = GetHospitals()
    obj.getHospitalsList(info[0],info[1],info[2])
    return json.dumps(obj.outp)
    
if __name__ == "__main__":
    app.run()
