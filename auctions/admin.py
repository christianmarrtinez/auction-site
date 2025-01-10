from django.contrib import admin
from .models import AuctionListing, Bid, Comment, Watchlist, Category, User


@admin.register(AuctionListing)
class AuctionListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'owner', 'current_price', 'created_at', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)

@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ('bidder', 'listing', 'amount', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('bidder__username', 'listing__title')
    ordering = ('-timestamp',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'listing', 'timestamp', 'content')
    list_filter = ('timestamp',)
    search_fields = ('author__username', 'listing__title', 'content')
    ordering = ('-timestamp',)


@admin.register(Watchlist)
class WatchlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'listing')
    search_fields = ('user__username', 'listing__title')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')