from django.db import models
from recruit.models import Recruit 

class Account(models.Model):
    name         = models.CharField(max_length=50)
    password     = models.CharField(max_length=100,null=True)
    email        = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20, null=True)
    education    = models.CharField(max_length=20, null=True)
    company      = models.CharField(max_length=20, null=True)
    created_at   = models.DateTimeField(auto_now_add=True)  
    updated_at   = models.DateTimeField(auto_now_add=True, null=True)
    kakao_id     = models.CharField(max_length=50, null=True)
    #like         = models.ManyToManyField('Recruit', through='Like', through_fields=('account','recruit'))

    class Meta:
        db_table = 'accounts'

class Resume(models.Model):
    user          = models.ForeignKey(Account, on_delete=models.CASCADE)    
    # main_category = models.ForeignKey(Recruit, on_delete=models.CASCADE)
    description   = models.CharField(max_length=100, null=True)
    title         = models.CharField(max_length=50,null=True)
    resume_status = models.CharField(max_length=50,null=True)
    created_at    = models.DateTimeField(auto_now_add=True, null=True)
    author        = models.CharField(max_length=50, null=True)
    email         = models.CharField(max_length=50, null=True)
    phone_number  = models.CharField(max_length=50, null=True)

    class Meta: 
        db_table = 'resumes'

class Career(models.Model):
    start_date   = models.DateField(max_length=10, null=True)
    end_date     = models.DateField(max_length=10, null=True)
    company_name = models.CharField(max_length=10, null=True)
    department   = models.CharField(max_length=10, null=True)
    resume       = models.ForeignKey(Resume, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'careers'

class Education(models.Model):
    start_date   = models.DateField(max_length=10, null=True)
    end_date     = models.DateField(max_length=10, null=True)
    college_name = models.CharField(max_length=10, null=True)
    major        = models.CharField(max_length=10, null=True)    
    contents     = models.CharField(max_length=10, null=True)
    resume       = models.ForeignKey(Resume, on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'educations'

class Like(models.Model):
    recruit = models.ForeignKey(Recruit, on_delete=models.CASCADE)
    user    = models.ForeignKey(Account, on_delete=models.CASCADE)
 
    class Meta: 
        db_table = 'likes'

class File(models.Model):
    user       = models.ForeignKey(Account, on_delete=models.CASCADE)
    file_url   = models.CharField(max_length=500,null=True)
    title      = models.CharField(max_length=50,null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = 'files' 