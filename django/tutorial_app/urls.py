
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$',views.index,name = 'index'),
    url(r'^static_page',views.static,name = 'static'),
    url(r'^template_example',views.templ_example,name = 'template_example'),
]
