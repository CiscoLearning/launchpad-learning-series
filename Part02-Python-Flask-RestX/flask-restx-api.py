import json
import random
from flask import Flask, request, jsonify
from flask_restx import Resource, Api, reqparse, fields
from tinydb import TinyDB, Query, where

"""
As every other extension, you can initialize it with an application object
"""
app = Flask(__name__)
api = Api(app, version='1.0', title='SIMPLE IPAM API',
          description='A simple IPAM API leveraging Flask-RESTX Library ', )
db = TinyDB('db/data.json')
ns = api.namespace('ipam', description='IPAM operations')

"""
Flask-RESTX’s request parsing interface, reqparse, is modeled after the argparse interface.
It’s designed to provide simple and uniform access to any variable on the flask.request object in Flask.
"""
parser = api.parser()
parser.add_argument("ip", type=str, required=True, help="Example - [10.10.100.5]", location="form")
parser.add_argument("netmask", type=str, required=True, help="Example - [255.255.255.0]", location="form")
parser.add_argument("vrf", type=str, required=True, help="Example - [Global, Admin, DMZ]", location="form")
parser.add_argument("status", type=str, required=True, help="Example - [Available, Reserved, Used]", location="form")



"""
HTTP methods defined as methods on your resource.
api.doc() decorator allows you to include additional information in the Swagger docs.
"""
@ns.route("/query")
@api.doc(responses={404: "query not found"})
@api.doc(responses={200: "success"})
class QueryRecords(Resource):
    def get(self):
        return jsonify(db.all())


@ns.route("/query/<ip>", endpoint="query")
@api.doc(params={'ip': 'Lookup a specific IP Address'})
@api.doc(responses={404: "query not found"})
@api.doc(responses={200: "success"})
class QuerySpecificRecords(Resource):
    def get(self, ip):
        for item in db:
            result = db.search(Query().ipadd == ip)
            if result:
                return jsonify(result)
            else:
                return jsonify(db.all())


@ns.route("/create")
@api.doc(responses={403: "failed to create"})
@api.doc(responses={201: "success"})
class CreateEntry(Resource):
    @api.doc(parser=parser)
    def post(self):
        args = parser.parse_args()
        db.insert(
            {"id": random.randint(1, 500), "ipadd": args['ip'], "mask": args['netmask'], "vrf": args['vrf'],
             "status": args['status']})
        return jsonify(db.all())


@ns.route("/update/<id>")
@api.doc(params={'id': 'Record ID to Update'})
class UpdateEntry(Resource):
    @api.doc(parser=parser)
    def put(self, id):
        args = parser.parse_args()
        db.update_multiple([
            ({'status': args['status']}, where('id') == int(id)),
            ({'ipadd': args['ip']}, where('id') == int(id)),
            ({'vrf': args['vrf']}, where('id') == int(id)),
            ({'mask': args['netmask']}, where('id') == int(id))
        ])
        return jsonify(db.all())


@ns.route("/delete/<id>")
@api.doc(params={'id': 'Record ID to Delete'})
class DeleteEntry(Resource):
    def delete(self, id):
        db.remove(Query().id == int(id))
        return jsonify(db.all())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105, debug=True)
