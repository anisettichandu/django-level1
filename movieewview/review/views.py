from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password,check_password
from django.views.decorators.csrf import csrf_exempt
import json
import jwt
from django.conf import settings
from datetime import datetime,timedelta
from zoneinfo import ZoneInfo
from review.models import Movie_details,Stu_details
# Create your views here.
def basic(request):
    return HttpResponse("hello world")

def movie_info(request):
    name=request.GET.get("name")
    date=request.GET.get("Date")
    return JsonResponse({"status":"Success","result":{"movie_name":name,"Release_date":date}})
    
@csrf_exempt
def movies(request):
    if request.method=="POST":
        data=json.loads(request.body)
        # data=request.POST
        Movie_details.objects.create(
            movie_name=data.get("movie_name"),
            release_date=data.get("release_date"),
            budget=data.get("budget"),
            rating=data.get("rating"))
        return JsonResponse({"status":"success","message":"inserted success","rating":data},status=200)
    elif request.method=="GET":
        new_rating=request.GET.get("new_rating")
        new_rating=float(new_rating)
        data1=Movie_details.objects.filter(rating__gt=new_rating).values()
        data1=list(data1)
        return JsonResponse({"status":"success","data":data1})
    # elif request.method=="GET":
    #     from_budget=request.GET.get("from_budget")
    #     from_budget=int(from_budget)
    #     to_budget=request.GET.get("to_budget")
    #     to_budget=int(to_budget)
    #     data=Movie_details.objects.all().values()
    #     result=[]
    #     for movies in data:
    #         b=movies["budget"]
    #         b=float(b[:-2])
    #         if from_budget<=b<=to_budget:
    #             result.append(movies)
    #     return JsonResponse({"status":"success","data":result})
    elif request.method=="PUT":
        data=json.loads(request.body)
        ref_id=data.get("id")
        if data.get("movie_name"):
            up=data.get("movie_name")
            exited=Movie_details.objects.get(id=ref_id)
            exited.movie_name=up
            exited.save()
            return JsonResponse({"status":"Success","update":"movie_name"})
        elif data.get("budget"):
            up=data.get("budgett")
            exited=Movie_details.objects.get(id=ref_id)
            exited.budget=up
            exited.save()
            return JsonResponse({"status":"Success","update":"budget"})
        elif data.get("rating"):
            up=data.get("rating")
            exited=Movie_details.objects.get(id=ref_id)
            exited.rating=up
            exited.save()
            return JsonResponse({"status":"Success","update":"rating"})
    elif request.method=="DELETE":
        data=json.loads(request.body)
        ref_id=data.get("id")
        new=Movie_details.objects.get(id=ref_id)
        new.delete()
        return JsonResponse({"status":"successs","message":"data deleted sucee"})
    return JsonResponse({"error":"error occured"},status=400)

@csrf_exempt
def student(request):
    if request.method=="POST":
        data=json.loads(request.body)
        
        Stu_details.objects.create(
        name=data.get("name"),
        email=data.get("email"),
        password=make_password(data.get("password")))
        return JsonResponse({"status":"success"},status=200)
    elif request.method=="GET":
        data=Stu_details.objects.all().values()
        data=list(data)
        return JsonResponse({"status":"Success","data":data})
@csrf_exempt
def log(request):
    if request.method=="POST":
        data=json.loads(request.body)
        issued_time=datetime.now(ZoneInfo("Asia/kolkata"))
        expired_time=issued_time+timedelta(hours=1)
        ref_id=data.get("ref_id")
        password=data.get("password")
        result=Stu_details.objects.get(id=ref_id)
        if check_password(password,result.password):
            payload={
                "name":result.name,
                "email":result.email,
                "password":result.password,
                "exp":int(expired_time.timestamp())
            }
            token=jwt.encode(payload,settings.SECRET_KEY,algorithm="HS256")
            return JsonResponse({"status":"login success","token":token,"issued":issued_time,"expired":expired_time,"expired in":int((expired_time-issued_time).total_seconds())})
        else:
            return JsonResponse({"result":"invalid"})
   
    elif request.method=="PUT":
        data=json.loads(request.body)
        ref_id=data.get("ref_id")
        up_password=data.get("up_password")
        exist=Stu_details.objects.get(id= ref_id)
        exist.password=make_password(up_password)
        exist.save()
        return JsonResponse({"status":"suvcesss"})
    elif request.method=="DELETE":
        data=json.loads(request.body)
        ref_id=data.get("ref_id")
        exist=Stu_details.objects.get(id= ref_id)
        exist.delete()
        return JsonResponse({"status":"Data deleted "},status=200)
    return JsonResponse({"error":"invalid"})
@csrf_exempt
def deo(request):
    if request.method=="GET":
        users=list(Stu_details.objects.values())
        print(request.token_data)
        for user in users:
            if user["name"]==request.token_data.get("name"):
                return JsonResponse({"status":"LoggedIn Success","data":users,"logged by":user["name"]})
        else:
            return JsonResponse({"status":"invalid user"})
    return JsonResponse({"status":"invalid"})
    
        # token=request.headers.get("Authorization")
    #     token_value=token.split(" ")[1]
    #     deco=jwt.decode(token_value,settings.SECRET_KEY,algorithms="HS256")
    #     return JsonResponse({"status":"success","data":deco})
    # return JsonResponse({"error":"invalid"})


    

    




        