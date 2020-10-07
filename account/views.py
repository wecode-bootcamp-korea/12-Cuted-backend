import json               
import bcrypt 
import jwt 
import requests
import boto3

from django.views import View 
from django.http import JsonResponse,HttpResponse
from django.db import IntegrityError

from my_settings import SECRET, ALGORITHM
from utils import login_decorator
from .models import Account, Resume, Career, Education, File, Like, Recruit


class EmailCheckView(View):
    def post(self,request):
        data = json.loads(request.body)
        try:
            if '@' not in data['email'] or '.' not in data ['email']:
                return JsonResponse(
                    {'message':'INVALID_EMAIL'},
                    status = 400
                )

            if Account.objects.filter(email=data['email']).exists():

                return JsonResponse(
                    {'message':'ALEADY_EXISTS'},
                    status = 200
                )
            
            return JsonResponse(
                {'message':'NEED_SIGNUP'},
                    status = 200
                )

        except KeyError:
            return JsonResponse(
                    {'message':'INVALID_KEY'},
                    status = 400
                )  
        
class SignUpView(View): 
    def post(self,request):
        data = json.loads(request.body)
        
        try: 
            if len(data['password']) < 6:
                return JsonResponse(
                    {'message':'INVALID_PASSWORD'},
                    status = 400 
                )
            if Account.objects.filter(phone_number=data['phone_number']).exists():

                return JsonResponse(
                    {'message':'ALREADY_EXISTS_PHONE_NUMBER'},
                    status = 400     
                )           
        
            encoded_password = data['password'].encode('utf-8')
            hashed_password  = bcrypt.hashpw(encoded_password,bcrypt.gensalt())
            data['password'] = hashed_password.decode('utf-8')
            
            Account.objects.create(
                email        = data['email'],
                name         = data['name'],
                phone_number = data['phone_number'],
                password     = data['password']
            )
            
            return JsonResponse(
                {'message':'SUCCESS'},
                status= 200
            )

        except IntegrityError:
            return JsonResponse(
                {'message':'ALREADY_EXISTS'},
                status = 400 
            )

        except KeyError:
            return JsonResponse(
                {'message':'INVALID_KEY'},
                status = 400
            )  

class SignInView(View): 
    def post(self,request):
        data = json.loads(request.body)

        try:
            if Account.objects.filter(email=data['email']).exists():
                user = Account.objects.get(email=data['email']) 
                
                if bcrypt.checkpw(data['password'].encode("utf-8"),user.password.encode("utf-8")):
                    token = jwt.encode({'email':data['email']},SECRET,algorithm=ALGORITHM).decode('utf-8') 

                    return JsonResponse(
                        {'ACCESS_TOKEN':token},
                        status = 200 
                    )
                
                return JsonResponse(
                    {'message':'INVALID_PASSWORD'},
                    status = 400
                )

        except KeyError:   
                return JsonResponse(
                    {'message': 'INVALID_KEY'},
                    status = 400
                )    

class KakaoSignInView(View):    
    def post(self,request):
        try: 
            access_token   = request.headers.get('Authorization')
            url            = 'https://kapi.kakao.com/v2/user/me'
            headers        = {'Authorization':f'Bearer {access_token}'}
            kakao_response = requests.get(url, headers=headers).json()
            kakao_id       = kakao_response.get('id')
            kakao_account  = kakao_response.get('kakao_account') 
            email          = kakao_account.get('email',None)
            kakao_profile  = kakao_account.get('profile')
            name           = kakao_profile.get('nickname')
        
            if Account.objects.filter(email=email).exists():
                user  = Account.objects.get(email=email)
                token = jwt.encode({'id':user.id},SECRET,algorithm=ALGORITHM)
                token = token.decode('utf-8')
                
                return JsonResponse(
                    {'token'  : token,
                    'message' : 'SUCCESS'}, 
                    status=200
                )
        
            else:
                Account.objects.create(
                    kakao_id = kakao_id,
                    email = email,
                    name = name
                )              

                token = jwt.encode({'email':email},SECRET,algorithm=ALGORITHM)
                token = token.decode('utf-8')
                
                return JsonResponse(
                    {'token'  : token,
                    'message' : 'SUCCESS'}, 
                    status=200
                )
        
        except IntegrityError:
                    return JsonResponse(
                        {'message':'ALREADY_EXISTS'},
                        status = 400 
                    )

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'},status = 400)      

class ResumeListView(View):
    @login_decorator
    def get(self,request):
        user        = request.user
        resume_list = Resume.objects.filter(email=user.email)                                                                                                        
        
        data = {'my_resume' : [{
                'id'            :resume.id, 
                'title'         : resume.title,
                'created_at'    : resume.created_at.strftime('%Y-%m-%d'),
                'resume_status' : resume.resume_status,
            }for resume in resume_list], 
        }

        return JsonResponse({'data':data}, status =200)

class ResumeDeleteView(View):        
    @login_decorator
    def delete(self,request,resume_id):
        try:
            Resume.objects.get(id=resume_id).delete()
            return JsonResponse({'message':'SUCCESS'},status=200)    
            
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'},status=401)

class ResumeWriteView(View):
    @login_decorator
    def get(self,request):
        try:
            if Account.objects.filter(email=request.user.email).exists():
                user = Account.objects.get(email=request.user.email)
                
                count = Account.objects.filter(email=user.email)[0].resume_set.count()
                
                resume = {
                    'title'        : f'{user.name}{count}',
                    'author'       : user.name,
                    'email'        : user.email,
                    'phone_number' : user.phone_number,
                }
                
                return JsonResponse({'resume':resume},status=200)
            return JsonResponse({'message':'INVALID_ID'},status=400)

        except KeyError:
            return JsonResponse({'message':'INVALID_KEY'},status=401)

class ResumeUpdateView(View):            
    @login_decorator
    def patch(self,request,resume_id):
        data = json.loads(request.body)
        user = request.user
        
        if Resume.objects.filter(id=resume_id).exists():
            
            if Resume.objects.get(id=resume_id).email != user.email:
                return JsonResponse({'message':'INVALID_ID'},status =400)

            try:
                resume = Resume.objects.get(id=resume_id)
                
                resume.title        = data['title']
                resume.author       = data['author']
                resume.email        = data['email']
                resume.phone_number = data['phone_number']
                resume.description  = data['description']
                resume.save()      

                updated_resume_json = {
                    'title' : resume.title ,
                    'author': resume.author,
                    'email' : resume.email,
                    'phone_number':resume.phone_number,
                    'description':resume.description
                }
                
                if data['career']:
                    for data in data['career']:
                        Career(
                            start_date   = data['start_date'],
                            end_date     = data['end_date'],
                            comapny_name = data['company_name'],
                            department   = data['department']
                        ).save()

                if data['education']:
                    for data in data['education']:
                        Education(
                            start_date    = data['start_date'],
                            end_date      = data['end_date'],
                            college_name  = data['college_name'],
                            major         = data['major'],
                            contents      = data['contents']
                        ).save()

                resume.resume_status ='작성 완료'
                print(resume.resume_status)
                return JsonResponse({'updated_resume':updated_resume_json},status=200)
            
            except Resume.DoesNotExist:
                return JsonResponse({'message' : 'UNKNOWN_RESUME'}, status = 404)

            except KeyError:
                return JsonResponse({'message':'KEY_ERROR'},status=401)       
        
        return JsonResponse({'message':'INVALID_ACCESS'},status=400)


class ResumeFileUploadView(View):
    s3_client = boto3.client('s3', aws_access_key_id='AKIAURLHDRRIAD4IHOWD', aws_secret_access_key='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')
    @login_decorator
    def post(self,request):
        file_urls=[]
        for file in request.FILES.getlist('file'):
            self.s3_client.upload_fileobj(
                file,'cutedimage',file.name,
                ExtraArgs={
                    'ContentType':file.content_type
                }
            )
            upload_file =File.objects.create(user=request.user ,title = file.name, file_url = 'https://s3.ap-northeast-2.amazonaws.com/cutedimage'+file.name)
            file_urls.append(upload_file.file_url)
              
        return JsonResponse({'files':file_urls}, status=200)

class LikeView(View):
    @login_decorator
    def post(self, request):
        data = json.loads(request.body)
        user = request.user
        recruit_id = data['recruit_id']
       
        if Like.objects.filter(user_id=user.id, recruit_id=recruit_id).exists():
            Like.objects.get(user_id=user.id, recruit_id=recruit_id).delete()
            return JsonResponse({'message':'DELETE'}, status=200)
        
        Like.objects.create(user_id=user.id, recruit_id =recruit_id)
        return JsonResponse({'message':'SUCCESS'})
    
    @login_decorator 
    def get(self, request):
        user = request.user
        like_recruit_list=  Like.objects.filter(user_id=user.id).select_related('recruit')
        
        recruit_list = [
            {
                "id"           : like_recruit.recruit.id,
                "thumbnail"    : like_recruit.recruit.thumbnail_url,
                "title"        : like_recruit.recruit.title,
                "company_name" : like_recruit.recruit.company_name,
                "location"     : like_recruit.recruit.location.name,
            }
        for like_recruit in like_recruit_list]
        return JsonResponse({'recruit_list' : recruit_list}, status=200) 