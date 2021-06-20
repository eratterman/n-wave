from django.urls import include, path
from rest_framework import routers
from . import views


router = routers.DefaultRouter()
router.register(r'asset', views.AssetViewSet)
router.register(r'column', views.ColumnViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('import/', views.ImportFilesView.as_view(), name='import'),
    path('plot/', views.PlotDataView.as_view(), name='plot'),
    path('plot_data/', views.ParquetGetView.as_view(), name='plot_data')
]
