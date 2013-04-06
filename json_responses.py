"""
Classes to build JSON body for REST API responses.

Response skeleton:
{
    'result': 'success|error',
    [ 'error': {
        'code': 'error_code',
        'message': 'Human readable message (optional).',
        [ specific error data ]
    } ],
    [ specific data ]
}

"""

import json
import flask


class JsonResponse(flask.Response):
    # Base class for an HTTP response containing arbitrary JSON content
    
    def __init__ (self, json_data=None):
    	# json_data must be 'json.dumps'-able
        flask.Response.__init__(
        	self,
        	json.dumps(json_data),
        	self.status_code,
        	None,
        	mimetype='text/json'
        )



class SuccessJsonResponse (JsonResponse):
    # JSON response for success (sets status to 'success' and appends specific
    # data)
    
    def __init__ (self, specific_data=None):
        self.status_code = 200
        json_data = { 'status': 'success' }
        if type(specific_data) is dict:
            json_data = dict(json_data.items() + specific_data.items()) 
        JsonResponse.__init__(self, json_data)



class ErrorJsonResponse (JsonResponse):
    # Base class for error JSON responses (sets status to 'error', builds
    # error part of the response and appends specific data
    def __init__ (self, error_code, error_message, error_data, specific_data):
        
        # Build error object
        error = { 'code': error_code }
        if error_message is not None:
            error['message'] = str(error_message)
        if type(error_data) is dict:
            error = dict(error.items() + error_data.items())
        
        # Build JSON response
        json_data = {'status': 'error', 'error': error}
        if type(specific_data) is dict:
            json_data = dict(json_data.items() + specific_data.items())
        
        JsonResponse.__init__(self, json_data)



class BadRequestJsonResponse (ErrorJsonResponse):
	# JSON response for HTTP 'bad request' (status code 400)
	# Use case: some GET or POST parameters are missing or have a bad syntax
	# (e.g. a number was expected and the provided value is a string)
    
    def __init__ (self, error_code, error_message='', error_details=None, specific_data=None):
        self.status_code = 400
        ErrorJsonResponse.__init__(self, error_code, error_message, error_details, specific_data)



class PreconditionFailedJsonResponse (ErrorJsonResponse):
    # JSON response for HTTP 'precondition failed' (status code 412)
    # Use case: unable to parse some GET or POST parameters, e.g. an ID was
    # provided but no matching item was found with this ID
    
    def __init__ (self, error_code, error_message='', error_details=None, specific_data=None):
        self.status_code = 412
        ErrorJsonResponse.__init__(self, error_code, error_message, error_details, specific_data)



class UnknownErrorJsonResponse (ErrorJsonResponse):
    # JSON response for other errors, HTTP status code 500
    
    def __init__ (self, error_message='', error_details=None, specific_data=None):
        self.status_code = 500
        ErrorJsonResponse.__init__(self, 'unknown', error_message, error_details, specific_data)


