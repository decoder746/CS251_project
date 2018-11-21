from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from mysite.core import views as core_views


urlpatterns = [
    url(r'^$', core_views.home, name='home'),
    url( r'^login/$',auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    url( r'^logout/$',auth_views.LoginView.as_view(template_name="login.html"), name="logout"),
    url(r'^signup/$', core_views.signup, name='signup'),
    url(r'^uploads/$', core_views.simple_upload, name='simple_upload'),
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
