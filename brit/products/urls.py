from django.urls import path, re_path

from products.views import ProductsViewSet

urlpatterns = [
    # URL pattern for creating a new product (POST request)
    path("list", ProductsViewSet.as_view({"post": "create"}), name="create_product"),
    # URL pattern for deleting a product by its primary key (DELETE request)
    re_path(
        "^product/(?P<pk>[0-9a-f]+)",
        ProductsViewSet.as_view({"delete": "destroy"}),
        name="delete_product",
    ),
]
