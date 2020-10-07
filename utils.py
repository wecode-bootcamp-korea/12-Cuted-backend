import json
import jwt

from django.http import JsonResponse
from my_settings import SECRET,ALGORITHM
from account.models import Account

def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):

        try:
            token = request.headers.get('Authorization', None)
            token_payload = jwt.decode(token, SECRET, algorithm = ALGORITHM)
            user = Account.objects.get(email = token_payload['email'])
            request.user = user

            return func(self, request, *args, **kwargs)       
        
        except jwt.exceptions.DecodeError:
            return JsonResponse({'message' : 'INVALID_TOKEN'}, status = 401)

        except Account.DoesNotExist:
            return JsonResponse({'message' : 'UNKNOWN_USER'}, status = 404)
            
        except KeyError:
            return JsonResponse({'message' : 'INVALID_KEY'}, status = 400)

    return wrapper