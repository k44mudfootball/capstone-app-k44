import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen

##Auth0 Application Info
AUTH0_DOMAIN = 'capstone-casting-k44.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'casting-info'

## AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


## Auth Header

def get_token_auth_header():
    ##Get the authorization header from the message
    auth = request.headers.get('Authorization', None)
    
    if not auth:
        ##Raise Auth Error if auth header is missing
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected.'
        }, 401)
    
    ##Split the header into parts: bearer, period, and token
    parts = auth.split()
    if parts[0].lower() != 'bearer':
        ##Raise Auth Error if the first part is not bearer
        raise AuthError({
            'code': 'malformed_header',
            'description': 'Header must start with bearer'
        }, 401)

    elif len(parts) == 1:
        ##Raise Auth Error if no token is found
        raise AuthError({
            'code': 'malformed_header',
            'description': 'Token not found.'
        }, 401)

    elif len(parts) > 2:
        ##Raise Auth Error if parts are greater than 2
        raise AuthError({
            'code': 'malformed_header',
            'description': 'Authorization header must be bearer token.'
        }, 401)

    token = parts[1]
    return token
   
##Check the permissions of the token
def check_permissions(permission, payload):
    if 'permissions' not in payload:
        ##Raise Auth Error if permissions were not included in payload
        raise AuthError({
            'code': 'invalid_permission',
            'description': 'Permissions were not included in the payload.'
        }, 400)
    
    if permission not in payload['permissions']:
        ##Raise Auth Error if permission string is not in payload permissions array
        raise AuthError({
            'code': 'invalid_permission',
            'description': 'Permission string is not in the payload permissions array'
        }, 403)
    
    return True

##Function to verify the decoded jwt
def verify_decode_jwt(token):
    ## Connects with the auth0 domain
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    ## verifies the RSA Key
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    ## Formats the payload of the RSA Key
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )
            return payload
        ## Checks for expired token
        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)
        ## Checks for invalid claims
        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
         ## Checks for valid header
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 400)


## Decorator method to implement authorization for the associated route
def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator