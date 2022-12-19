from django.urls import re_path, path
from .views import CategoriesListView, DiscountsListView, ProducersListView, \
    ProductItemsListView, PromocodesListView, CategoryProductsView, ProducerProductView, \
    DiscountProductsView, RegistrationView, ActivateAccountView

urlpatterns = [
    re_path(r'^categories-all', CategoriesListView.as_view(), name='categories-all'),
    re_path(r'^discounts-all', DiscountsListView.as_view()),
    re_path(r'^producers-all', ProducersListView.as_view()),
    re_path(r'^products-all', ProductItemsListView.as_view()),
    re_path(r'^promocodes-all', PromocodesListView.as_view()),
    path('category/<int:cat_id>/', CategoryProductsView.as_view()),
    path('producer/<int:producer_id>/', ProducerProductView.as_view()),
    path('discount/<int:discount_id>/', DiscountProductsView.as_view()),
    re_path(r'^register/', RegistrationView.as_view()),
    path('activate/<slug:uidb64>/<slug:token>/', ActivateAccountView.as_view(), name='activate')

]
