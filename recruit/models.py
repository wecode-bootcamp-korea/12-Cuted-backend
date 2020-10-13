from django.db import models
from datetime  import datetime
# from account.models import Like

class MainCategory(models.Model):
    name   = models.CharField(max_length=45)

    class Meta:
        db_table = 'main_categories'

class Category(models.Model):
    name            = models.CharField(max_length=45)
    main_category   = models.ForeignKey(MainCategory, on_delete=models.CASCADE)
    category_image  = models.CharField(max_length=500,null=True)

    class Meta:
        db_table = 'categories'

class SubCategory(models.Model):
    name               = models.CharField(max_length=45)
    category           = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory_image  = models.CharField(max_length=500, null=True)

    class Meta:
        db_table = 'sub_categories'

class Salary(models.Model):
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    years       = models.CharField(max_length=45)
    salary      = models.IntegerField(default=0)

    class Meta:
        db_table = 'salaries'

class Location(models.Model):
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'location'

class DetailLocation(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    name     = models.CharField(max_length=45)

    class Meta:
        db_table = 'detail_location'

class Recruit(models.Model):
    title                  = models.CharField(max_length=45)
    thumbnail_url          = models.CharField(max_length=500)
    company_name           = models.CharField(max_length=45)
    location               = models.ForeignKey(Location, on_delete=models.CASCADE)
    detail_location        = models.ForeignKey(DetailLocation, on_delete=models.CASCADE)
    reward                 = models.IntegerField(default=0)
    intro                  = models.TextField()
    due_date               = models.DateTimeField(auto_now_add=True, blank=True)
    work_area              = models.TextField()
    subcategory            = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    main_work              = models.TextField()
    condition              = models.TextField()
    preferential_treatment = models.TextField(default="prefer")
    map_url                = models.CharField(max_length=500)
    benefits               = models.TextField()
    response_rate          = models.IntegerField(null=True)
    latitude               = models.FloatField(null=True)
    longitude              = models.FloatField(null=True)
<<<<<<< HEAD

=======
>>>>>>> 50eb482... Add : ListView, SalaryView, Fix : DetailView, SearchView
    class Meta:
        db_table = 'recruits'

class RecommendRecruit(models.Model):
    recruit             = models.ForeignKey(Recruit, on_delete=models.CASCADE, related_name = 'recruit')
    recommend_recruit   = models.ForeignKey(Recruit, on_delete=models.CASCADE, related_name = 'recommend_recruit')

    class Meta:
        db_table = 'recommend_recruit'