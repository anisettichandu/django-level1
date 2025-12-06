from django.http import HttpResponse
from django.http import JsonResponse
from django.conf import settings
import jwt
import json

class movie_info:
    def __init__(self,get_response):
        self.get_response=get_response
    def __call__(self,request):
        if (request.path=="/movies/"  and  request.method=="POST"): 
            data=json.loads(request.body)
            # data=request.POST
            if not data.get("movie_name"):
                return JsonResponse({"Status":"movie_name required"})
            elif not data.get("budget"):
                return JsonResponse({"Status":"budget required"})
            elif not data.get("rating"):
                return JsonResponse({"Status":"rating required"})
            elif not data.get("release_date"):
                return JsonResponse({"Status":"release_date required"})
        return self.get_response(request)
class cheching:
    def __init__(self,get_response):
        self.get_response=get_response
    def __call__(self,request):
        if request.path=="/deo/":
            token=request.headers.get("Authorization")
            if not token:
                return JsonResponse({"error":"Token is missing"},status=400)
            token_value=token.split(" ")[1]
            try:
                decoded_data=jwt.decode(token_value,settings.SECRET_KEY,algorithms=["HS256"])
                request.token_data=decoded_data
            except jwt.ExpiredSignatureError:
                return JsonResponse({"error":"Token has expired please login again"},status=400)
            except jwt.exceptions.InvalidSignatureError:
                return JsonResponse({"error":"invalid Token Signature"},status=400)
        return self.get_response(request)                
            
            
        