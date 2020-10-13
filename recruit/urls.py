"""cuted URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path,include
from .views      import DetailView, SearchView, SalaryView, ListView
urlpatterns = [
    path('/detail/<int:recruit_id>', DetailView.as_view()),
    path('/search', SearchView.as_view()),
    path('/salary', SalaryView.as_view()),
    path('/', ListView.as_view()),
    path('/<int:category>/<int:subcategory>', ListView.as_view())

]
