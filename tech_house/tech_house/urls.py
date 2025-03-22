"""
URL configuration for tech_house project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path,include
from django.conf import settings 
from django.conf.urls.static import static
import debug_toolbar


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('ecommerce.urls')),
    path('ecommerce/ecommerce_api/',include('ecommerce.ecommerce_api.urls')),
    path('store/',include('manager.urls')),
    path('__debug__/', include(debug_toolbar.urls)),
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('allauth.socialaccount.urls')),
]

if settings.DEBUG:
    
    urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)

admin.site.site_header = 'Koshtech Systems'                    # default: "Django Administration"
admin.site.index_title = 'Admin page'                 # default: "Site administration"
admin.site.site_title = 'koshtech admin'