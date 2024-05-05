import os
import requests
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configure MySQL from environment variables
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST', 'localhost')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER', 'admin')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD', 'admin')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB', 'bd')

@app.route('/')
def index():
    return render_template('index.html')

# Initialize MySQL
mysql = MySQL(app)

@app.route('/gnss_data', methods=['POST'])
def create_gnss_data():
    cur = mysql.connection.cursor()
    data = request.get_json()
    print(data)
    Svid = data.get('Svid')
    ConstellationType = data.get('ConstellationType')
    TimeOffsetNanos = data.get('TimeOffsetNanos')
    State = data.get('State')
    ReceivedSvTimeNanos = data.get('ReceivedSvTimeNanos')
    ReceivedSvTimeUncertaintyNanos = data.get('ReceivedSvTimeUncertaintyNanos')
    Cn0DbHz = data.get('Cn0DbHz')
    PseudorangeRateMetersPerSecond = data.get('PseudorangeRateMetersPerSecond')
    PseudorangeRateUncertaintyMetersPerSecond = data.get('PseudorangeRateUncertaintyMetersPerSecond')
    AccumulatedDeltaRangeState = data.get('AccumulatedDeltaRangeState')
    AccumulatedDeltaRangeMeters = data.get('AccumulatedDeltaRangeMeters')
    AccumulatedDeltaRangeUncertaintyMeters = data.get('AccumulatedDeltaRangeUncertaintyMeters')
    CarrierFrequencyHz = data.get('CarrierFrequencyHz')
    MultipathIndicator = data.get('MultipathIndicator')
    CarrierFreqHz = data.get('CarrierFreqHz')

    cur.execute("INSERT INTO gnss_data (Svid, ConstellationType, TimeOffsetNanos, State, ReceivedSvTimeNanos, ReceivedSvTimeUncertaintyNanos, Cn0DbHz, PseudorangeRateMetersPerSecond, PseudorangeRateUncertaintyMetersPerSecond, AccumulatedDeltaRangeState, AccumulatedDeltaRangeMeters, AccumulatedDeltaRangeUncertaintyMeters, CarrierFrequencyHz, MultipathIndicator, CarrierFreqHz) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (Svid, ConstellationType, TimeOffsetNanos, State, ReceivedSvTimeNanos, ReceivedSvTimeUncertaintyNanos, Cn0DbHz, PseudorangeRateMetersPerSecond, PseudorangeRateUncertaintyMetersPerSecond, AccumulatedDeltaRangeState, AccumulatedDeltaRangeMeters, AccumulatedDeltaRangeUncertaintyMeters, CarrierFrequencyHz, MultipathIndicator, CarrierFreqHz))
    mysql.connection.commit()
    cur.close()
    return jsonify({"status": "success"}, 201)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
