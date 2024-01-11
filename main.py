
from flask import Flask, jsonify, request,render_template
#from db import get_info, add_info,update_info, delete_info
from db import get_info, insert_diagnosed,insert_regularCheckup,insert_vaccination,get_upcomingDoseInfo,get_diagnosedInfo,get_upcomingDoseInfo,get_diagnosedInfo

app = Flask(__name__)

@app.route('/regularCheckup', methods=['POST'])
def info():
    if request.method == 'POST':
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400  

        insert_regularCheckup(request.get_json())
        return 'Info Added'
    
@app.route('/vaccination', methods=['POST'])
def info():
    if request.method == 'POST':
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400  

        insert_vaccination(request.get_json())
        return 'Info Added'

@app.route('/diagnosed', methods=['POST'])
def info():
    if request.method == 'POST':
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400  

        insert_diagnosed(request.get_json())
        return 'Info Added'

    

@app.route('/info')
def view():
    info = get_info()
    return render_template('viewVaccine.html', data=info)   

@app.route('/diagnosedDetails')
def view():
    info = get_info()
    return render_template('viewDiagnosed.html', data=info)   

@app.route('/analytics')
def view():
    info = get_info()
    return render_template('viewAnalytics.html', data=info)   

if __name__ == '__main__':
    app.run()




