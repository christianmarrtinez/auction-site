from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create_listing"),
    path("categories/", views.categories, name="categories"),
    path("categories/<int:category_id>/", views.category_listings, name="category_listings"),
    path("active", views.active_listings, name="active_listings"),
    path("listing/<int:listing_id>/", views.listing, name="listing"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("listing/<int:listing_id>/edit/", views.edit_listing, name="edit_listing"),
    path("watchlist/<int:listing_id>/toggle/", views.toggle_watchlist, name="toggle_watchlist")

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)