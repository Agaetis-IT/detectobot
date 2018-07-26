# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify, request
from app.views.dto import InputsSchema
from app.functions.runDetection import RunDetection
from config import params
from cerberus import Validator
import logging
import json
import requests

_logger = logging.getLogger(__name__)
api = Blueprint('pv', __name__)

class InputsException(Exception):
    pass

@api.route('/', methods=["GET"])
def info():
    res = jsonify({"info": "service is runing"})

    res.status_code = 200
    return res

@api.route('/detection', methods=["POST"])
def detection():
    try:
        _logger.debug(request.get_json(silent=True))
        inputs = request.get_json(silent=True)

        v = Validator(InputsSchema)
        imagesList = []
        for image in inputs:
            if v.validate(image):
                imagesList.append(image) 
            else:
                image[params['output.detection']] = {'ERROR missing inputs':"Not found or incorrect inputs"}
                r = requests.post(params['url.error'], data=image)
        if len(imagesList) == 0:
            raise InputsException
                
        output = RunDetection(imagesList)
                
        res = jsonify(output)
        res.status_code = 200
        return res

    except InputsException:
        res = jsonify({"ERROR nothing to do":"No picture to tag"})
        res.status_code = 400
        return res

    return jsonify({})
