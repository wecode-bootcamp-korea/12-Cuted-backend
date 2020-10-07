import json
import bcrypt
import jwt

from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile

from unittest.mock import patch, MagicMock 
from my_settings import SECRET, ALGORITHM
from utils import login_decorator
from .models import Account, Resume, Career, Education, File


class EmailCheckTest(TestCase):
    
    def setUp(self):
        Account.objects.create(
            email = 'hongse@naver.com'
        )

    def tearDown(self):
        Account.objects.all().delete()

    def test_emailcheck_post_aleady_exists(self):
        client = Client()
        account = {
            'email' : 'hongse@naver.com',
        }
        response = client.post('/account/emailcheck', json.dumps(account), content_type='application/json')

        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json(),
            {
                'message':'ALEADY_EXISTS'  
            }
        )

    def test_emailcheck_post_need_signup(self):
        client = Client()
        account = {
            'email' : 'hong@gmail.com'
        }
        response = client.post('/account/emailcheck', json.dumps(account), content_type='application/json')

        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json(),
            {
                'message':'NEED_SIGNUP'  
            }
        )

    def test_emailcheck_post_invalid_keys(self):
        client = Client()
        account = {
            'e-mail' : 'hong@gmail.com'
        }
        response = client.post('/account/emailcheck', json.dumps(account), content_type='application/json')

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json(),
            {
                'message':'INVALID_KEY'
            }
        )

    def test_emailcheck_post_invalid_email(self):
        client = Client()
        account = {
            'email': 'honggmailcom' 
        }
        response = client.post('/account/emailcheck', json.dumps(account), content_type='application/json')

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json(),
            {
                'message':'INVALID_EMAIL'
            }
        )

class SingupTest(TestCase):

    def setUp(self):
        bytes_pw = bytes('12345678','utf-8')
        hashed_pw = bcrypt.hashpw(bytes_pw, bcrypt.gensalt())
        
        Account.objects.create(
            name = 'hong',
            password = hashed_pw.decode('UTF-8'),
            email = 'hong@gmail.com',
            phone_number = '01012341234'
        )
    
    def tearDown(self):
        Account.objects.all().delete()

    def test_signupview_post_success(self):
        client = Client()
        account = {
            'name'         : 'hong2',
            'password'     : '12345678',
            'email'        : 'hong2@gmail.com',
            'phone_number' : '01012345678'
        }
        response = client.post('/account/emailcheck/signup', json.dumps(account), content_type='application/json')

        self.assertEqual(response.status_code,200)

    def test_signup_post_aleady_exists(self):
        client = Client()
        account = {
            'name'        : 'hong',
            'password'    : '12345678',
            'email'       : 'hong@gmail.com',
            'phone_number': '01012341234'
        }
        response = client.post('/account/emailcheck/signup', json.dumps(account), content_type='application/json')

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json(),
            {
                'message':'ALREADY_EXISTS_PHONE_NUMBER'  
            }
        )

    def test_signup_post_invalid_keys(self):
        client = Client()
        account = {
            'first_name'  : 'hong',
            'pasword'     : '12345678',
            'email'       : 'hong@gmail.com',
            'phone_number': '01012341234' 
        }
        response = client.post('/account/emailcheck/signup', json.dumps(account), content_type='application/json')

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json(),
            {
                'message':'INVALID_KEY'
            }
        )

class SignInTest(TestCase):

    def setUp(self):
        bytes_pw = bytes('12345678','utf-8')
        hashed_pw = bcrypt.hashpw(bytes_pw,bcrypt.gensalt())
        
        user = Account.objects.create(
            name = 'hong',
            password = hashed_pw.decode('UTF-8'),
            email = 'hong@gmail.com',
            phone_number = '01012341234'
        )
        
        self.token = jwt.encode({'email':user.email},SECRET,algorithm=ALGORITHM).decode('utf-8') 

    def tearDown(self):
        Account.objects.all().delete()    
    
    def test_signinview_get_success(self):
        client = Client()
        user = Account.objects.get( name = 'hong')

        account = {
            'id'           : user.id,
            'name'         : 'hong',
            'password'     : '12345678',
            'email'        : 'hong@gmail.com',
            'phone_number' : '01012341234'
        }
       
        response = client.post('/account/emailcheck/signin', json.dumps(account), content_type='application/json')
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json(),
            {
                'ACCESS_TOKEN': self.token
            }
        )

    def test_signinview_get_invalid_password(self):
        client = Client()
        account = {
            'name'        : 'hong',
            'password'    : '12341234',
            'email'       : 'hong@gmail.com',
            'phone_number': '01012341234'
        }
        response = client.post('/account/emailcheck/signin', json.dumps(account), content_type='application/json')

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json(),
            {
                'message':'INVALID_PASSWORD'  
            }
        )

    def test_signinview_get_invalid_keys(self):
        client = Client()
        account = {
            'name'         : 'hong',
            'passwrd'      : '12345678',
            'email'        : 'hong@gmail.com',
            'phone_number' : '01012341234' 
        }
        response = client.post('/account/emailcheck/signin', json.dumps(account), content_type='application/json')
        self.assertEqual(response.json(),
            {
                'message':'INVALID_KEY'
            }
        ) 
        self.assertEqual(response.status_code,400)

class KakaoSignInTest(TestCase):
    
    def setUp(self):
        Account.objects.create(
            kakao_id = '1499',
            name     = '홍성은',
            email    = 'hongse21@gmail.com',
        ) 
    def teardown(self):
        Account.objects.all.delete()
    
    @patch('account.views.requests')
    def test_kakao_sign_in(self,mocked_requests):
        client = Client()
        
        class MockedResponse:
            def json(self):
                return{
                    'id'      : 1499, 
                    'kakao_account': { 
                    'profile': {
                        'nickname': '홍성은',
                    },'email': 'hongse21@gmail.com'}
                }
                           
        mocked_requests.get = MagicMock(return_value = MockedResponse())
        
        test = {
            'kakao_id' : 1499, 
            'email'    : 'hongse21@gmail.com',
            'name'     : '홍성은',
            }

        response = client.post('/account/emailcheck/kakaosignin',json.dumps(test), **{'Authorization':'1234', 'content_type':'application/json'})
        self.assertEqual(response.status_code,200)

class ResumeListTest(TestCase):
    maxDiff=None
    def setUp(self):
        user = Account.objects.create(id=1, name='hong', email='hong@gmail.com')
        Resume.objects.create(user_id=1, email=user.email, title='안녕하세요',resume_status='작성중',author='hong')

        self.token = jwt.encode({'email':user.email},SECRET,algorithm=ALGORITHM).decode('UTF-8')                
          
    def tearDown(self):
        Account.objects.all().delete()
        Resume.objects.all().delete()

    def test_resumelist_get_success(self):       
        client  = Client()
        headers = {'HTTP_Authorization':self.token}
        user    = Account.objects.create(id=2, name='hong2',email='h2ong@gmail.com')

        data = {'my_resume' : [{
                'id' : 2,  
                'title' : '안녕하세요',
                'created_at' : user.created_at.strftime('%Y-%m-%d'),
                'resume_status' : '작성중'
            }] 
        }
        
        response = client.get('/account/resumelist', **headers)
        self.assertEqual(response.json(),{'data':data})
        self.assertEqual(response.status_code,200)

class ResumeDeleteTest(TestCase):
    maxDiff=None
    def setUp(self):
        user = Account.objects.create(name='hong')
        Resume.objects.create(user = user, title='안녕하세요',resume_status='작성중',author='hong')
        
        self.token = jwt.encode({'email':user.email},SECRET,algorithm=ALGORITHM).decode('UTF-8')                
          
    def tearDown(self):
        Account.objects.all().delete()
        Resume.objects.all().delete()
             
    def test_resumelist_delete_(self):
        client  = Client()
        headers = {'HTTP_Authorization':self.token}
        
        response = client.delete('/account/resumedelete/1', **headers)
        
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json(),
            {
                'message':'SUCCESS'  
            }
        )

class ResumeWriteTest(TestCase):
    maxDiff=None
    def setUp(self):
        user = Account.objects.create(name='hong',email='hong@gmail.com',phone_number='01012341234')
        Resume.objects.create(id=1, title ='hong1',user=user) 
    
        self.token = jwt.encode({'email':user.email},SECRET,algorithm=ALGORITHM).decode('UTF-8')                
          
    def tearDown(self):
        Account.objects.all().delete()
        Resume.objects.all().delete()
             
    def test_resumewrite_post_(self):
        client  = Client()
        headers = {'HTTP_Authorization':self.token}
        user    = Account.objects.create(id=1, name='hong',email='hong2@gmail.com',phone_number='01012341234')
        count   = Resume.objects.filter(author=user.name).count()
        
        resume = { 
            'title'        : 'hong'+ str(count),
            'author'       : 'hong',
            'email'        : 'hong@gmail.com',
            'phone_number' : '01012341234'
        } 

        response = client.get('/account/resumewrite',**headers)
        
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json(),
            {
              'resume':resume  
            }
        )

class ResumeFileUploadTest(TestCase):

    def setUp(self):
        user  = Account.objects.create(id=1, name='hong',email='hong@gmail.com')
        self.token = jwt.encode({'email':user.email},SECRET,algorithm=ALGORITHM).decode('UTF-8')                
          
    def tearDown(self):
        Account.objects.all().delete()

    @patch('account.views.ResumeFileUploadView.s3_client')
    def test_upload(self, mocked_client):
        
        client  = Client()
        headers = {'HTTP_Authorization':self.token}
        
        image_mock = SimpleUploadedFile('Hell_Row_World.png', b'file_content', content_type='png')

        response = client.post('/account/resumelist/fileupload',
        {'file':image_mock},format ='multipart', **headers)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 
                {'files': ['https://s3.ap-northeast-2.amazonaws.com/cutedimageHell_Row_World.png']
                }
        )       