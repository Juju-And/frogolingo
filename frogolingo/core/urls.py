"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.conf.urls import url

from django.conf import settings
from django.conf.urls.static import static

from datasets.views import (MainView,
                            AddNewExpressionView,
                            DeleteExpressionView,
                            MessagesView,
                            StatsView,
                            AllExpressionsView,
                            EditExpressionView,
                            AddExpressionView
                            )
from learning.views import (TrainingView,
                            LearningView,
                            NextExpressionsView,
                            NextExpressionTrainView
                            )
from users.views import (LoginView,
                         CreateUserView,
                         logoutUser)

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', MainView.as_view(), name="index"),
    url(r'^login', LoginView.as_view()),
    url(r'^logout', logoutUser),
    url(r'^create_user', CreateUserView.as_view()),
    url(r'^create_expression', AddNewExpressionView.as_view()),
    url(r'^delete_expression/(?P<expression_id>(\d)+)$', DeleteExpressionView.as_view()),
    url(r'^learn', LearningView.as_view()),
    url(r'^training', TrainingView.as_view()),
    url(r'^messages', MessagesView.as_view()),
    url(r'^stats', StatsView.as_view()),
    url(r'^all_expressions', AllExpressionsView.as_view()),
    url(r'^next_expression_train', NextExpressionTrainView.as_view()),
    url(r'^next_expression', NextExpressionsView.as_view()),
    url(r'^edit_expression/(?P<pk>(\d)+)$', EditExpressionView.as_view()),

    url(r'^add_expression', AddExpressionView.as_view()),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
