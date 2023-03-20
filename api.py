from flask import Flask, jsonify, request
import uuid
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

samples = []

def calculate(mp10, mp25, co, ozonio, no2, so2):
    if mp10 == '':
        qualidade_mp = 0
    elif mp10 != '':
        mp10 = float(mp10)
        if mp10 <= 50:
            qualidade_mp = 1    
        elif 50 < mp10 <= 100:
            qualidade_mp = 2
        elif 100 < mp10 <= 150:
            qualidade_mp = 3
        elif 150 < mp10 <= 250:
            qualidade_mp = 4
        else:
            qualidade_mp = 5

    #classificação particulas pequenas
    if mp25 == '':
        qualidade_mpp = 0
    elif mp25 != '':
        mp25 = float(mp25)
        if mp25 <= 25:
            qualidade_mpp = 1
        elif mp25 <= 50:
            qualidade_mpp = 2
        elif mp25 <= 75:
            qualidade_mpp = 3
        elif mp25 <= 125:
            qualidade_mpp = 4
        else:
            qualidade_mpp = 5

    #classificação ozonio
    if ozonio == '':
        qualidade_o3 = 0
    elif ozonio != '':
        ozonio = float(ozonio)
        if ozonio <= 100:
            qualidade_o3 = 1
        elif ozonio <= 130:
            qualidade_o3 = 2
        elif ozonio <= 160:
            qualidade_o3 = 3
        elif ozonio <= 200:
            qualidade_o3 = 4
        else:
            qualidade_o3 = 5

    #classificação CO
    if co == '':
        qualidade_co = 0
    elif co != '':
        co = float(co)
        if co <= 9:
            qualidade_co = 1
        elif co <= 11:
            qualidade_co = 2
        elif co <= 13:
            qualidade_co = 3
        elif co <= 15:
            qualidade_co = 4
        else:
            qualidade_co = 5

    #classificação NO2
    if no2 == '':
        qualidade_no2 = 0
    elif no2 != '':
        no2 = float(no2)
        if no2 <= 200:
            qualidade_no2 = 1
        elif no2 <= 240:
            qualidade_no2 = 2
        elif no2 <= 320:
            qualidade_no2 = 3
        elif no2 <= 1130:
            qualidade_no2 = 4
        else:
            qualidade_no2 = 5

    #classificação SO2
    if so2 == '':
        qualidade_so2 = 0
    elif so2 != '':
        so2 = float(so2)
        if so2 <= 20:
            qualidade_so2 = 1
        elif so2 <= 40:
            qualidade_so2 = 2
        elif so2 <= 365:
            qualidade_so2 = 3
        elif so2 <= 800:
            qualidade_so2 = 4
        else:
            qualidade_so2 = 5

    lista = [qualidade_mp, qualidade_mpp, qualidade_o3, qualidade_co, qualidade_no2, qualidade_so2]
    qualidade = 0

    for i in range(0, 6):
        if list[i] == '':
            i+1
        if lista[i] > qualidade:
            qualidade = lista[i]
    
    return qualidade


@app.route('/samples/', methods=['POST'])
def new_sample():
    
    new_sample = request.get_json()
    new_sample["id"] = int(uuid.uuid4())
    mp10, mp25, co, ozonio, no2, so2 = new_sample["mp10"], new_sample["mp25"], new_sample["co"], new_sample["ozonio"], new_sample["no2"], new_sample["so2"],
    
    if mp10 == None:
        mp10 = ''
    if mp25 == None:
        mp25 = ''
    if co == None:
        co = ''
    if ozonio == None:
        ozonio = ''
    if no2 == None:
        no2 = ''
    if so2 == None:
        so2 = ''
    new_sample["pureza"] = calculate(mp10, mp25, co, ozonio, no2, so2)
    samples.append(new_sample)
    return jsonify(samples)

@app.route('/samples', methods=['GET'])
def list_sample():
    return jsonify(samples)
        
@app.route('/samples/<int:id>', methods=['PUT'])
def edit_sample_by_id(id):
    changes = request.get_json()
    
    for index, sample in enumerate(samples):
        if sample.get('id') == id:
            samples[index].update(changes)
            sample = samples[index]
            mp10, mp25, co, ozonio, no2, so2 = sample["mp10"], sample["mp25"], sample["co"], sample["ozonio"], sample["no2"], sample["so2"]
            pureza = calculate(mp10, mp25, co, ozonio, no2, so2)
            sample["pureza"] = pureza
            samples[index].update(sample)
            return jsonify(samples[index])
        
@app.route('/samples/<int:id>', methods=['DELETE'])
def delete_sample(id):
    for index, sample in enumerate(samples):
        if sample.get('id') == id:
            del samples[index]
            return jsonify(samples)

app.run(port=5000, host="localhost", debug=True)
