import json
import bcrypt

from django.test       import TestCase
from django.test       import Client

from recruit.models    import MainCategory,Category,SubCategory,Location,DetailLocation,Recruit,RecommendRecruit,Salary

class RecruitDetailViewTest(TestCase):
    def setUp(self):
        client = Client()
        MainCategory.objects.create(name="test_main")
        Category.objects.create(name="test_category", main_category=MainCategory.objects.get(name="test_main"), category_image = "test_image")
        SubCategory.objects.create(name="test_sub", category=Category.objects.get(name="test_category"), subcategory_image="test_sub_image")
        Location.objects.create(name="seoul")
        DetailLocation.objects.create(location = Location.objects.get(name="seoul"), name="gangnam")
        Recruit.objects.create(
            id = 1,
            title="web_developer",
            thumbnail_url = "test_url",
            company_name="wecode",
            reward = 100,
            intro="test_intro",
            work_area = "test_area",
            main_work = "test_main_work",
            condition = "test_condition",
            subcategory = SubCategory.objects.get(name="test_sub"),
            preferential_treatment = "test_prefer",
            location = Location.objects.get(name="seoul"),
            detail_location = DetailLocation.objects.get(name="gangnam"),
            benefits = "test_benefit",
            latitude = 37.479289,
            longitude = 126.978159
        )

        Recruit.objects.create(
            id = 2,
            title="front_developer",
            thumbnail_url = "test_url",
            company_name="wecode",
            reward = 100,
            intro="test_intro",
            work_area = "test_area",
            main_work = "test_main_work",
            condition = "test_condition",
            subcategory = SubCategory.objects.get(name="test_sub"),
            preferential_treatment = "test_prefer",
            location = Location.objects.get(name="seoul"),
            detail_location = DetailLocation.objects.get(name="gangnam"),
            benefits = "test_benefit",
            latitude = 37.479289,
            longitude = 126.978159
        )
        RecommendRecruit.objects.create(recruit_id=1, recommend_recruit_id=2)

    def tearDown(self):
        MainCategory.objects.all().delete()
        Category.objects.all().delete()
        SubCategory.objects.all().delete()
        Location.objects.all().delete()
        DetailLocation.objects.all().delete()
        Recruit.objects.all().delete()
        RecommendRecruit.objects.all().delete()

    def test_detailview_get_success(self):
        self.maxDiff = None
        client = Client()
        data = {
                "id"          : 1,
                "title"       : "web_developer",
                "intro"       : "test_intro",
                "company_name": "wecode",
                "location"    : "seoul",
                "main_work"   : "test_main_work",
                "condition"   : "test_condition",
                "prefer"      : "test_prefer",
                "due_date"    : str(Recruit.objects.get(id=1).due_date)[0:10],
                "work_area"   : "test_area",
                "benefit"     : "test_benefit",
                "latitude"    : 37.479289,
                "longitude"   : 126.978159,
                "recommend_recruit" : [
                    {
                        "id"                  : 2,
                        "recommend_thumbnail" : "test_url",
                        "recommend_title"     : "front_developer",
                        "recommend_company"   : "wecode",
                        "recommend_location"  : "seoul"
                    }
                ]
        }
        response = client.get('/recruit/detail/1')
        self.assertEqual(response.json(), {"detail_list" : data})
        self.assertEqual(response.status_code, 200)  

    def test_detailview_get_not_found(self):
        client = Client()
        response = client.get('/recruit/detail/3')
        self.assertEqual(response.json(), {"message" : 'no recruit'})
        self.assertEqual(response.status_code, 400)  

class RecruitSearchViewTest(TestCase):
    def setUp(self):
        client = Client()
        MainCategory.objects.create(name="test_main")
        Category.objects.create(name="test_category", main_category=MainCategory.objects.get(name="test_main"), category_image = "test_image")
        SubCategory.objects.create(name="test_sub", category=Category.objects.get(name="test_category"), subcategory_image="test_sub_image")
        Location.objects.create(name="seoul")
        DetailLocation.objects.create(location = Location.objects.get(name="seoul"), name="gangnam")
        Recruit.objects.create(
            id = 1,
            title="web_developer",
            thumbnail_url = "test_url",
            company_name="wecode",
            reward = 100,
            intro="test_intro",
            work_area = "test_area",
            main_work = "test_main_work",
            condition = "test_condition",
            subcategory = SubCategory.objects.get(name="test_sub"),
            preferential_treatment = "test_prefer",
            location = Location.objects.get(name="seoul"),
            detail_location = DetailLocation.objects.get(name="gangnam"),
            benefits = "test_benefit",
            latitude = 37.479289,
            longitude = 126.978159
        )

        Recruit.objects.create(
            id = 2,
            title="front_developer",
            thumbnail_url = "test_url",
            company_name="wecode",
            reward = 100,
            intro="test_intro",
            work_area = "test_area",
            main_work = "test_main_work",
            condition = "test_condition",
            subcategory = SubCategory.objects.get(name="test_sub"),
            preferential_treatment = "test_prefer",
            location = Location.objects.get(name="seoul"),
            detail_location = DetailLocation.objects.get(name="gangnam"),
            benefits = "test_benefit",
            latitude = 37.479289,
            longitude = 126.978159
        )

    def tearDown(self):
        MainCategory.objects.all().delete()
        Category.objects.all().delete()
        SubCategory.objects.all().delete()
        Location.objects.all().delete()
        DetailLocation.objects.all().delete()
        Recruit.objects.all().delete()
        

    def test_searchview_get_success(self):
        self.maxDiff = None
        client = Client()
        data = [{
                 "id"            : 1,
                 "thumbnail_url" : "test_url",
                 "title"         : "web_developer",
                 "company_name"  : "wecode",
                 "location"      : "seoul",
        },
        {
                 "id"            : 2,
                 "thumbnail_url" : "test_url",
                 "title"         : "front_developer",
                 "company_name"  : "wecode",
                 "location"      : "seoul",
        }]

        response = client.get('/recruit/search?keyword=developer')
        self.assertEqual(response.json(), {'recruit_list' : data })
        self.assertEqual(response.status_code, 200)  

    def test_searchview_get_empty_word(self):
        self.maxDiff = None
        client = Client()
        response = client.get('/recruit/search?keyword=')
        self.assertEqual(response.json(), {'message' : 'EMPTY_WORD'})
        self.assertEqual(response.status_code, 400)  

    def test_searchview_get_no_found(self):
        self.maxDiff = None
        client = Client()
        response = client.get('/recruit/search?keyword=back')
        self.assertEqual(response.json(), {'message' : 'recruit_list doesn\'t exist'})
        self.assertEqual(response.status_code, 400)  


class RecruitSalaryViewTest(TestCase):
    def setUp(self):
        client = Client()
        MainCategory.objects.create(name="test_main")
        Category.objects.create(name="test_category", main_category=MainCategory.objects.get(name="test_main"), category_image = "test_image")
        SubCategory.objects.create(id=1,name="test_sub", category=Category.objects.get(name="test_category"), subcategory_image="test_sub_image")
        Location.objects.create(name="seoul")
        DetailLocation.objects.create(location = Location.objects.get(name="seoul"), name="gangnam")
        Recruit.objects.create(
            id = 1,
            title="web_developer",
            thumbnail_url = "test_url",
            company_name="wecode",
            reward = 100,
            intro="test_intro",
            work_area = "test_area",
            main_work = "test_main_work",
            condition = "test_condition",
            subcategory = SubCategory.objects.get(name="test_sub"),
            preferential_treatment = "test_prefer",
            location = Location.objects.get(name="seoul"),
            detail_location = DetailLocation.objects.get(name="gangnam"),
            benefits = "test_benefit",
            latitude = 37.479289,
            longitude = 126.978159
        )

        Recruit.objects.create(
            id = 2,
            title="front_developer",
            thumbnail_url = "test_url",
            company_name="wecode",
            reward = 100,
            intro="test_intro",
            work_area = "test_area",
            main_work = "test_main_work",
            condition = "test_condition",
            subcategory = SubCategory.objects.get(name="test_sub"),
            preferential_treatment = "test_prefer",
            location = Location.objects.get(name="seoul"),
            detail_location = DetailLocation.objects.get(name="gangnam"),
            benefits = "test_benefit",
            latitude = 37.479289,
            longitude = 126.978159
        )

        Salary.objects.create(subcategory_id=1, years="new", salary=3000)
        Salary.objects.create(subcategory_id=1, years="first", salary=4000)


    def tearDown(self):
        MainCategory.objects.all().delete()
        Category.objects.all().delete()
        SubCategory.objects.all().delete()
        Location.objects.all().delete()
        DetailLocation.objects.all().delete()
        Recruit.objects.all().delete()
        

    def test_salaryview_get_success(self):
        self.maxDiff = None
        client = Client()
        salary_list = [{'year' : "new", "salary" : 3000}, {"year" : "first", "salary" : 4000 }]
        recruit_list = [
            {
                "id" : 1,
                "thumbnail_url" : "test_url",
                "title" : "web_developer",
                "company_name" : "wecode",
                "location" : "seoul"
            },
            {
                "id" : 2,
                "thumbnail_url" : "test_url",
                "title" : "front_developer",
                "company_name" : "wecode",
                "location" : "seoul"

            }
        ]
        response = client.get('/recruit/salary?sub=1')
        self.assertEqual(response.json(), {'salary_list' : salary_list, 'recruit_list' : recruit_list})
        self.assertEqual(response.status_code, 200)  

    def test_salaryview_get_no_found(self):
        self.maxDiff = None
        client = Client()
        salary_list = [{'year' : "new", "salary" : 3000}, {"year" : "first", "salary" : 4000 }]
        recruit_list = [
            {
                "id" : 1,
                "thumbnail_url" : "test_url",
                "title" : "web_developer",
                "company_name" : "wecode",
                "location" : "seoul"
            },
            {
                "id" : 2,
                "thumbnail_url" : "test_url",
                "title" : "front_developer",
                "company_name" : "wecode",
                "location" : "seoul"

            }
        ]
        response = client.get('/recruit/salary?sub=1')
        self.assertEqual(response.json(), {'salary_list' : salary_list, 'recruit_list' : recruit_list})
        self.assertEqual(response.status_code, 200)  

    def test_salaryview_get_no_found(self):
        self.maxDiff = None
        client = Client()
        response = client.get('/recruit/salary?sub=5')
        self.assertEqual(response.json(), {'message' : 'NO_ITEM'})
        self.assertEqual(response.status_code, 400)  

class RecruitListViewTest(TestCase):
    def setUp(self):
        client = Client()
        MainCategory.objects.create(id=1,name="test_main")
        Category.objects.create(id=1,name="test_category", main_category=MainCategory.objects.get(name="test_main"), category_image = "test_image")
        SubCategory.objects.create(id=1,name="test_sub", category=Category.objects.get(name="test_category"), subcategory_image="test_sub_image")
        Location.objects.create(id=1,name="seoul")
        DetailLocation.objects.create(id=1, location = Location.objects.get(name="seoul"), name="gangnam")
        Recruit.objects.create(
            id = 1,
            title="web_developer",
            thumbnail_url = "test_url",
            company_name="wecode",
            reward = 100,
            intro="test_intro",
            work_area = "test_area",
            main_work = "test_main_work",
            condition = "test_condition",
            subcategory = SubCategory.objects.get(name="test_sub"),
            preferential_treatment = "test_prefer",
            location = Location.objects.get(name="seoul"),
            detail_location = DetailLocation.objects.get(name="gangnam"),
            benefits = "test_benefit",
            latitude = 37.479289,
            longitude = 126.978159,
            response_rate=95
        )

        Recruit.objects.create(
            id = 2,
            title="front_developer",
            thumbnail_url = "test_url",
            company_name="wecode",
            reward = 100,
            intro="test_intro",
            work_area = "test_area",
            main_work = "test_main_work",
            condition = "test_condition",
            subcategory = SubCategory.objects.get(name="test_sub"),
            preferential_treatment = "test_prefer",
            location = Location.objects.get(name="seoul"),
            detail_location = DetailLocation.objects.get(name="gangnam"),
            benefits = "test_benefit",
            latitude = 37.479289,
            longitude = 126.978159,
            response_rate=95
        )

    def tearDown(self):
        MainCategory.objects.all().delete()
        Category.objects.all().delete()
        SubCategory.objects.all().delete()
        Location.objects.all().delete()
        DetailLocation.objects.all().delete()
        Recruit.objects.all().delete()
        

    def test_listview_get_data(self):
        self.maxDiff = None
        client = Client()
        recruit_list = [
            {
                "id" : 1,
                "thumbnail_url" : "test_url",
                "title" : "web_developer",
                "company_name" : "wecode",
                "location" : "seoul",
                "response_rate" : 95
            },
            {
                "id" : 2,
                "thumbnail_url" : "test_url",
                "title" : "front_developer",
                "company_name" : "wecode",
                "location" : "seoul",
                "response_rate" : 95
            }
        ]

        menu_list = [
            {
                "id" : 1,
                "name" : "test_sub",
                "image": "test_sub_image"
            }
        ]


        response = client.get('/recruit/1/1?location=1&detail_location=1')
        self.assertEqual(response.json(), {'data' : {'recruit_list' : recruit_list, 'menu_list' : menu_list}})
        self.assertEqual(response.status_code, 200)  