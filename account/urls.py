from django.urls import path
from .views import (EmailCheckView, 
                    SignUpView, 
                    SignInView, 
                    KakaoSignInView, 
                    ResumeListView,
                    ResumeDeleteView,
                    ResumeWriteView,
                    ResumeUpdateView,
                    ResumeFileUploadView,
                    LikeView)

urlpatterns = [
    path('/emailcheck', EmailCheckView.as_view()),
    path('/emailcheck/signup', SignUpView.as_view()),
    path('/emailcheck/signin', SignInView.as_view()),
    path('/emailcheck/kakaosignin', KakaoSignInView.as_view()),
    path('/resumelist',ResumeListView.as_view()),
    path('/resumedelete/<int:resume_id>',ResumeDeleteView.as_view()),
    path('/resumewrite',ResumeWriteView.as_view()),
    path('/resumeupdate/<int:resume_id>',ResumeUpdateView.as_view()),
    path('/resumelist/fileupload',ResumeFileUploadView.as_view()),
    path('/like',LikeView.as_view())
]