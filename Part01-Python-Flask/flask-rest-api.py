import json
from flask import Flask, request, jsonify
from tinydb import TinyDB, Query, where
import random

app = Flask(__name__)
db = TinyDB('db/data.json')


@app.route('/')
def index():
    return ("Welcome to Launchpad 🚀 - Flask APP is up and running on {}".format(request.host_url))


@app.route('/query', methods=['GET'])
def query_records():
    ip = request.args.get('ip')
    for item in db:
        result = db.search(Query().ipadd == ip)
        if result:
            return jsonify(result)
        else:
            return jsonify(db.all())


@app.route('/create', methods=['POST'])
def create_record():
    record = json.loads(request.data)
    result = db.insert({"id": random.randint(1,500), "ipadd": record['ipadd'], "mask": record['mask'], "vrf": record['vrf'], "status": record['status']})
    return jsonify(db.all())


@app.route('/update', methods=['PUT'])
def update_record():
    record = json.loads(request.data)
    rec_id = request.args.get('id')
    db.update_multiple([
        ({'status': record['status']}, where('id') == int(rec_id)),
        ({'ipadd': record['ipadd']}, where('id') == int(rec_id)),
        ({'vrf': record['vrf']}, where('id') == int(rec_id)),
        ({'mask': record['mask']}, where('id') == int(rec_id))
    ])
    return jsonify(db.all())


@app.route('/remove', methods=['DELETE'])
def delete_record():
    rec_id = request.args.get('id')
    db.remove(Query().id == int(rec_id))
    return jsonify(db.all())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105, debug=True)