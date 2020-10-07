from django.db import models
# from recruit.models import Recruit 

class Account(models.Model):
    name         = models.CharField(max_length=50)
    password     = models.CharField(max_length=10)
    email        = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)
    education    = models.CharField(max_length=20, null=True)
    company      = models.CharField(max_length=20, null=True)
    created_at   = models.DateTimeField(auto_now_add=True)  
    updated_at   = models.DateTimeField(auto_now_add=True, null=True)
    # like         = models.ManyToManyField('Recruit', through='Like', through_fields=('account','recruit'))
    # book_mark    = models.ManyToManyField('Recruit', through='BookMark', through_fields=('account','recruit')) 

    class Meta:
        db_table = 'accounts'

class Career(models.Model):
    start_date   = models.DateField(max_length=10, null=True)
    end_date     = models.DateField(max_length=10, null=True)
    company_name = models.CharField(max_length=10, null=True)
    department   = models.CharField(max_length=10, null=True)

    class Meta:
        db_table = 'careers'

class Education(models.Model):
    start_date   = models.DateField(max_length=10, null=True)
    end_date     = models.DateField(max_length=10, null=True)
    college_name = models.CharField(max_length=10, null=True)
    major        = models.CharField(max_length=10, null=True)    
    contents     = models.CharField(max_length=10, null=True)
  
    class Meta: 
        db_table = 'educations'

class Resume(models.Model):
    user          = models.ForeignKey(Account, on_delete=models.CASCADE)    
    career        = models.ForeignKey(Career, on_delete=models.CASCADE) 
    education     = models.ForeignKey(Education, on_delete=models.CASCADE)
    file_url      = models.CharField(max_length=100, null=True)
    # main_category = models.ForeignKey(Recruit, on_delete=models.CASCADE)
    description   = models.CharField(max_length=100, null=True)

    class Meta: 
        db_table = 'resumes'

# class Like(models.Model):
    # recruit = models.ForeignKey(Recruit, on_delete=models.CASCADE)
    # user    = models.ForeignKey(Account, on_delete=models.CASCADE)

    # class Meta: 
        # db_table = 'likes'

# class BookMark(models.Model):
    # recruit = models.ForeignKey(Recruit, on_delete=models.CASCADE)
    # user    = models.ForeignKey(Account, on_delete=models.CASCADE)

    # class Meta: 
        # db_table = 'book_marks'

class Application_status(models.Model):
    reusme  = models.ForeignKey(Resume, on_delete=models.CASCADE)
    user    = models.ForeignKey(Account, on_delete=models.CASCADE)
    # recruit = models.ForeignKey(Recruit, on_delete=models.CASCADE)

    class Meta: 
        db_table = 'application_status'