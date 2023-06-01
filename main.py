
from flask import Flask, jsonify, request,render_template
from db import get_info, add_info,update_info, delete_info

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET','PUT','DELETE'])
def info():
    if request.method == 'POST':
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400  

        add_info(request.get_json())
        return 'Info Added'
    
    if request.method == 'PUT':
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400
        
        payload = request.get_json()
        patient_id = payload.pop('PatientID', None)
        if patient_id is None:
            return jsonify({"msg": "Missing PatientID in request"}), 400
        update_info(patient_id, payload)
        return 'Info Updated'
    
    if request.method == 'DELETE':
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400
        
        payload = request.get_json()
        patient_id = payload.get('PatientID')
        if patient_id is None:
            return jsonify({"msg": "Missing PatientID in request"}), 400
        delete_info(patient_id)
        return 'Info Deleted'

@app.route('/view')
def view():
    info = get_info()
    return render_template('view.html', data=info)   

if __name__ == '__main__':
    app.run()




