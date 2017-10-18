from django.conf.urls import url

from .views import charge_point, PointCheckoutAjaxView, PointImpAjaxView

urlpatterns = [
    url(r'^charge/$', charge_point),
    url(r'^checkout/$', PointCheckoutAjaxView.as_view(), name='point_checkout'),
    url(r'^validation/$', PointImpAjaxView.as_view(), name='point_validation'),
]