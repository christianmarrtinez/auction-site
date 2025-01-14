from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import pytz

class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name

class AuctionListing(models.Model):
    CATEGORY_CHOICES = [
        ('Fashion', 'Fashion'),
        ('Toys', 'Toys'),
        ('Electronics', 'Electronics'),
        ('Home', 'Home'),
        
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    image = models.ImageField(upload_to='listing_images/', blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, blank=True, null=True)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="listings", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # Automatically set the category_id based on the category field value
        if self.category:
            self.category_id = Category.objects.get(name=self.category)
        super().save(*args, **kwargs)

class Bid(models.Model):
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="bids")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.amount} on {self.listing.title} by {self.bidder.username}"

class Comment(models.Model):
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.timestamp:  # If timestamp is not set yet (on creation)
            # Convert the current time to EST before saving
            eastern = pytz.timezone('US/Eastern')
            self.timestamp = timezone.now().astimezone(eastern)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.listing.title}"

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="watchlist_entries")

    class Meta:
        unique_together = ('user', 'listing') 