from django.conf.urls import url

from .views import ProductFormView

urlpatterns = [
    url(
        regex=r"^(?P<product_code>[A-Za-z0-9\-]+)/$",
        view=ProductFormView.as_view(),
        name="product_form"
    ),
]
