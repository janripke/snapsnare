import logging
from flask import request, current_app
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from snapsnare.system import responsify, tracer
from snapsnare.repositories.property.property_repository import PropertyRepository


class ShowProperty(Resource):

    @jwt_required()
    def get(self):
        try:
            connector = current_app.connector

            name = request.args.get('name')

            if not name:
                return responsify(message='property name is required'), 400

            property_repository = PropertyRepository(connector)
            property_ = property_repository.find_by(name=name)

            if not property_:
                return responsify(message='property not found'), 404

            return responsify(property=property_), 200
        except Exception:
            response = tracer.build()
            logging.exception('show property failed')
            return response, 500


