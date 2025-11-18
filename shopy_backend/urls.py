from django.urls import path
from .views import ProductListView,UserCartView, AddItemCartView, RemoveItemCartView

urlpatterns = [
    path("getItems", ProductListView.as_view(), name="product-list"),

    path("cart/user/<int:user_id>/", UserCartView.as_view(), name="user-cart"),
    path("cart/addItem/<int:user_id>/", AddItemCartView.as_view(), name="add-cart-item"),
    path("cart/removeItem/<int:user_id>/<int:item_code>/", RemoveItemCartView.as_view(), name="remove-cart-item"),
]
