from django.views          import View
from django.http           import JsonResponse
from django.db             import models
from django.db.models      import Q

from recruit.models        import (MainCategory, Category, SubCategory, Salary, Location, DetailLocation, Recruit, RecommendRecruit)

class DetailView(View):
    def get(self, request, recruit_id):
        try :
            recruit = Recruit.objects.prefetch_related('location', 'recommend_recruit').get(id=recruit_id)
        except Recruit.DoesNotExist:
            return JsonResponse({'message' : 'no recruit'}, status = 400)
        
        recruit_info ={
            "id"          : recruit.id,
            "title"       : recruit.title,
            "intro"       : recruit.intro,
            "company_name": recruit.company_name,
            "location"    : recruit.location.name,
            "main_work"   : recruit.main_work,
            "condition"   : recruit.condition,
            "prefer"      : recruit.preferential_treatment,
            "due_date"    : str(recruit.due_date)[:10],
            "work_area"   : recruit.work_area,
            "benefit"     : recruit.benefits,
            "latitude"    : recruit.latitude,
            "longitude"   : recruit.longitude,
            "recommend_recruit" : [
                {
                    "id"                  : recommend.recommend_recruit.id,
                    "recommend_thumbnail" : recommend.recommend_recruit.thumbnail_url,
                    "recommend_title"     : recommend.recommend_recruit.title,
                    "recommend_company"   : recommend.recommend_recruit.company_name,
                    "recommend_location"  : recommend.recommend_recruit.location.name
                }
            for recommend in recruit.recruit.all()]
        }
        return JsonResponse({'detail_list' : recruit_info}, status = 200)

class SearchView(View):
    def get(self, request):
        word = request.GET.get('keyword', None)
        if not word:
            return JsonResponse({'message' : 'EMPTY_WORD'}, status=400)
        recruit = Recruit.objects.filter(title__icontains=word).prefetch_related('location')
        recruit_list = [
            {
                 "id"            : recruit_item.id,
                 "thumbnail_url" : recruit_item.thumbnail_url,
                 "title"         : recruit_item.title,
                 "company_name"  : recruit_item.company_name,
                 "location"      : recruit_item.location.name,
            }
        for recruit_item in recruit]

        if not recruit_list:
            return JsonResponse({'message' : 'recruit_list doesn\'t exist'}, status=400)

        return JsonResponse({'recruit_list' : recruit_list}, status = 200)

class ListView(View):
    def get(self, request, category=None, subcategory=None): 
        order_method    = request.GET.get('order', None)
        location        = request.GET.get('location', None)
        detail_location = request.GET.get('detail_location', None)
        
        if not category:
            recruit = Recruit.objects.all()
            menu = Category.objects.all()
            menu_list = [
                { "id" : menu_item.id,
                  "name" : menu_item.name,
                  "image" : menu_item.category_image} for menu_item in menu]
        else :
            recruit = Recruit.objects.filter(subcategory_id = subcategory)
            menu = SubCategory.objects.filter(category_id__id = category)
            menu_list = [
                { "id" : menu_item.id,
                  "name" : menu_item.name,
                  "image" : menu_item.subcategory_image} for menu_item in menu]

        recruit = recruit.prefetch_related('location')

        if location:
            if not location or not detail_location == "0":
                if detail_location:
                    recruit = recruit.filter(location_id=location,detail_location_id=detail_location)
                else :
                    recruit = recruit.filter(location_id=location)
            
        if order_method == "date":
            recruit = recruit.order_by('-due_date')
        elif order_method == "response":
            recruit = recruit.order_by('response_rate')

        recruit_list = [
            {
                 "id"            : recruit_item.id,
                 "thumbnail_url" : recruit_item.thumbnail_url,
                 "title"         : recruit_item.title,
                 "company_name"  : recruit_item.company_name,
                 "location"      : recruit_item.location.name,
                 "response_rate" : recruit_item.response_rate
            }
        for recruit_item in recruit]
        return JsonResponse({'data' : {"recruit_list" : recruit_list, "menu_list" : menu_list}}, status = 200)

class SalaryView(View):
    def get(self, request):
        sub = request.GET.get('sub', None)
        if not Salary.objects.filter(subcategory_id=sub).exists():
            return JsonResponse({'message' : 'NO_ITEM'}, status=400)
            
        salary_set = Salary.objects.filter(subcategory_id = sub).select_related('subcategory')
        recruit = Recruit.objects.all().prefetch_related('location')

        salary_list = [{
            'year'   : item.years,
            'salary' : item.salary
        }for item in salary_set]

        recruit_list = [
            {
                 "id"            : recruit_item.id,
                 "thumbnail_url" : recruit_item.thumbnail_url,
                 "title"         : recruit_item.title,
                 "company_name"  : recruit_item.company_name,
                 "location"      : recruit_item.location.name
            }
        for recruit_item in recruit]
        
        return JsonResponse({'salary_list' : salary_list, 'recruit_list' : recruit_list}, status=200)