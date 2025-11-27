from django.http import HttpResponse
from django.http import JsonResponse
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