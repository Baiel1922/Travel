from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib import admin
from django.urls import path, include

schema_view = get_schema_view(
    openapi.Info(
        title='Authentication API',
        default_version='v1',
        description='Test Description',
    ),
    public=True
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('post/', include('post.urls')),
    path('p/', include('comment.urls')),
]
