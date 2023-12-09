from django.contrib import admin
from django.urls import path
from summoners.views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", insert_summoner),
    path("summoner/<str:name>/<str:tag_line>", summoner),
]
