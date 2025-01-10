from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import AuctionListingForm, BidForm, CommentForm
from django.db.models import Max
from django.utils import timezone
import pytz

from .models import User, AuctionListing, Watchlist, Bid, Comment, Category


def index(request):
    listings = AuctionListing.objects.filter(is_active=True)

    # Dynamically calculate current price for each listing
    listings_with_prices = []
    for listing in listings:
        highest_bid = listing.bids.aggregate(Max('amount'))['amount__max']  # Get the highest bid amount
        current_price = highest_bid if highest_bid else listing.starting_bid  # Use starting_bid if no bids
        listings_with_prices.append({
            'listing': listing,
            'current_price': current_price,
        })

    context = {
        'listings_with_prices': listings_with_prices,
    }
    return render(request, 'auctions/index.html', context)


def login_view(request):
    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

       
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def create_listing(request):
    if request.method == "POST":
        form = AuctionListingForm(request.POST, request.FILES)  # Include request.FILES to handle file uploads
        if form.is_valid():
            listing = form.save(commit=False)
            listing.owner = request.user  
            if listing.category_id:
                listing.category = listing.category_id.name
            listing.save()
            return redirect('index')  
    else:
        form = AuctionListingForm()
    return render(request, 'auctions/create_listing.html', {'form': form})


def active_listings(request):
    listings = AuctionListing.objects.filter(is_active=True)
    return render(request, "auctions/active_listings.html", {
        "listings": listings
    })

def listing(request, listing_id):
    listing = get_object_or_404(AuctionListing, id=listing_id)
    bids = listing.bids.order_by('-amount')  # Get all bids for this listing, ordered by amount descending

    current_price = bids.first().amount if bids.exists() else listing.starting_bid

    # Get the time in the user's timezone (assuming user is logged in)
    if request.user.is_authenticated:
        user_timezone = pytz.timezone('US/Eastern')  # Defaulting to EST
    else:
        user_timezone = pytz.timezone('UTC')  # Use UTC for unauthenticated users

    # Adjust the timestamps
    comments = listing.comments.all().order_by('-timestamp')
    for comment in comments:
        comment.timestamp = comment.timestamp.astimezone(user_timezone)  # Convert timestamp to user's timezone

    winner = None
    is_user_winner = False
    if not listing.is_active and bids.exists():
        # Get the highest bid
        winner_bid = bids.first()
        if winner_bid:
            winner = winner_bid.bidder  # The bidder who placed the highest bid
            # Check if the logged-in user is the winner
            if request.user.is_authenticated and request.user == winner:
                is_user_winner = True


    if request.method == 'POST':
    # Handle placing a bid
        if 'close_auction' in request.POST:
            if request.user == listing.owner:
                listing.is_active = False  # Close the auction
                listing.save()
                messages.success(request, "Auction has been closed.")
                return redirect('listing', listing_id=listing.id)


    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to place a bid.")
            return redirect('login')

        form = BidForm(request.POST)
        if form.is_valid():
            bid_amount = form.cleaned_data['amount']

            # Validate the bid
            if bid_amount < listing.starting_bid:
                messages.error(request, "Your bid must be at least the starting bid.")
            elif bids.exists() and bid_amount <= bids.first().amount:
                messages.error(request, "Your bid must be higher than the current highest bid.")
            else:
                # Save the bid
                new_bid = form.save(commit=False)
                new_bid.listing = listing
                new_bid.bidder = request.user
                new_bid.save()

                # Update the current price of the listing
                listing.current_price = bid_amount
                listing.save()

                messages.success(request, "Your bid was placed successfully.")
                return redirect('listing', listing_id=listing_id)
            
            # Handle comment submission
        if 'comment' in request.POST:
            comment_content = request.POST.get('comment_content')
            if comment_content:
                comment = Comment(listing=listing, author=request.user, content=comment_content)
                comment.save()
                messages.success(request, "Your comment was added.")
                return redirect('listing', listing_id=listing.id)

    else:
        form = BidForm()

    # Get the list of users in the watchlist for this listing
    listing_watchlist_users = listing.watchlist_entries.values_list('user', flat=True)

   # Get all comments for the listing
    comments = listing.comments.all().order_by('-timestamp')  # Fetch comments ordered by timestamp

    context = {
        'listing': listing,
        'bids': bids,
        'form': form,
        'current_price': current_price,
        'listing_watchlist_users': listing_watchlist_users,
        'winner': winner,
        'is_user_winner': is_user_winner,  
        'comments': comments,  
    }
    return render(request, 'auctions/listing.html', context)

@login_required
def toggle_watchlist(request, listing_id):
    listing = get_object_or_404(AuctionListing, id=listing_id)

    action = request.POST.get('action')
    if action == "add":
        # Add to watchlist if not already present
        if not Watchlist.objects.filter(user=request.user, listing=listing).exists():
            Watchlist.objects.create(user=request.user, listing=listing)
            messages.success(request, f'"{listing.title}" added to your watchlist.')
    elif action == "remove":
        # Remove from watchlist if present
        Watchlist.objects.filter(user=request.user, listing=listing).delete()
        messages.success(request, f'"{listing.title}" removed from your watchlist.')

     # Get the updated list of users in the watchlist for this listing
    listing_watchlist_users = listing.watchlist_entries.values_list('user', flat=True)
  
    return redirect("listing", listing_id=listing.id)

@login_required
def close_auction(request, listing_id):
    # Get the auction listing object
    auction = get_object_or_404(AuctionListing, id=listing_id)

    # Check if the user is the creator of the auction
    if auction.owner != request.user:
        return redirect('auction_detail', listing_id=auction.id)

    # Ensure the auction is still active before closing
    if not auction.is_active:
        return redirect('auction_detail', listing_id=auction.id)

    # Mark the auction as closed
    auction.is_active = False

    # Find the highest bid
    highest_bid = auction.bids.order_by('-amount').first()  # Get the highest bid
    if highest_bid:
        auction.current_price = highest_bid.amount
        auction.save()

    # Redirect to the auction's detail page
    return redirect('auction_detail', listing_id=auction.id)

@login_required
def watchlist(request):
    # Get all listings in the user's watchlist
    watchlist_items = Watchlist.objects.filter(user=request.user)
    listings_with_prices = []

    for item in watchlist_items:
        listing = item.listing
        highest_bid = listing.bids.aggregate(Max('amount'))['amount__max']
        current_price = highest_bid if highest_bid else listing.starting_bid
        listings_with_prices.append({
            'listing': listing,
            'current_price': current_price,
        })

    context = {
        'listings_with_prices': listings_with_prices,
    }
    return render(request, 'auctions/watchlist.html', context)
def categories(request):
    categories = Category.objects.all()
    return render(request, 'auctions/categories.html', {'categories': categories})

def category_listings(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    listings = AuctionListing.objects.filter(category_id=category, is_active=True)
    return render(request, 'auctions/category_listings.html', {
        'category': category,
        'listings': listings
    })
