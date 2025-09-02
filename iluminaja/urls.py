from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from rest_framework import routers
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny
from django.urls import re_path
from rest_framework import permissions

from cadastro_poste.views_api import PosteViewSet, LampadaViewSet
from manutencao.views_api import ManutencaoViewSet
from usuarios.views_api import UsuarioViewSet

router = routers.DefaultRouter()
router.register(r'postes', PosteViewSet)
router.register(r'lampadas', LampadaViewSet)
router.register(r'manutencoes', ManutencaoViewSet)
router.register(r'usuarios', UsuarioViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="IluminaJá API",
        default_version='v1',
        description="API para gestão de postes, lâmpadas, manutenções e usuários",
        contact=openapi.Contact(email="suporte@iluminaja.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('cadastro_poste/', include('cadastro_poste.urls')),
    path('usuarios/', include('usuarios.urls')),
    path('manutencao/', include('manutencao.urls')),

    path('api/', include(router.urls)),


    path('swagger/', schema_view.with_ui('swagger',
         cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc',
         cache_timeout=0), name='schema-redoc'),


    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


    path('', RedirectView.as_view(url='/cadastro_poste/', permanent=False)),

    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
]
