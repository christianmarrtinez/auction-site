from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import AuctionListingForm

from .models import User, AuctionListing, Watchlist


def index(request):
    listings = AuctionListing.objects.filter(is_active=True)

    return render(request, "auctions/index.html", {
        "listings": listings
    })


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
        form = AuctionListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.owner = request.user  
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

    # Get the list of users in the watchlist for this listing
    listing_watchlist_users = listing.watchlist_entries.values_list('user', flat=True)
   # listing_watchlist_users = listing.watchlist_entries.values_list('user__id', flat=True)


    context = {
        'listing': listing,
        'listing_watchlist_users': listing_watchlist_users,  # pass it to the template
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

