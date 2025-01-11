Features Implemented

1. Models

The application includes the following models:

User: Extends Django's AbstractUser to manage user authentication and additional fields.

Listing: Represents an auction listing with fields such as title, description, starting bid, current bid, category, image, and creation date.

Bid: Tracks bids placed by users on listings.

Comment: Stores user comments on listings.

2. User Authentication

Users can register, log in, and log out.

The layout dynamically changes based on whether a user is authenticated (user.is_authenticated).

3. Creating Listings

Users can create auction listings by providing:

Title

Description

Starting bid

Optional image URL

Optional category

4. Active Listings Page

The default route displays all currently active auction listings.

Each listing includes:

Title

Description

Current price

Image (if available)

5. Listing Page

Each listing has its own page displaying:

Title

Description

Current price

Bidding functionality

Comment section

Watchlist management

Users can:

Add or remove the listing from their watchlist.

Place a bid (must meet the minimum criteria).

Close the auction (if they are the owner).

View the winner of a closed auction.

6. Watchlist

A page for signed-in users to view all listings they have added to their watchlist.

7. Categories

A page displaying all available categories.

Clicking on a category shows all active listings within that category.

8. Admin Interface

Site administrators can:

View, add, edit, and delete listings, bids, and comments.

Manage categories and users.

9. Additional Features

Listing owners can edit their listings.

Commenting functionality on listing pages.

Technical Details

1. Django Framework

The project leverages Django for its robust features, including models, views, templates, and authentication.

2. Database and Migrations

The project uses SQLite as its database.

![Screen Shot 2025-01-11 at 4 54 25 PM](https://github.com/user-attachments/assets/ef704803-907f-4e4f-bd8f-202c5f6bb8a6)
![Screen Shot 2025-01-11 at 4 54 34 PM](https://github.com/user-attachments/assets/504d8cfe-6270-4fff-ab95-d7a691a3dee8)
![Screen Shot 2025-01-11 at 4 56 17 PM](https://github.com/user-attachments/assets/51130b48-1e6b-4dcf-b2b6-f92b28baf9d9)
![Screen Shot 2025-01-11 at 4 54 12 PM](https://github.com/user-attachments/assets/db8e8af7-205d-41ff-87b6-31d44bb68d6a)
![Screen Shot 2025-01-11 at 4 54 44 PM](https://github.com/user-attachments/assets/46f8bfc9-4e54-4993-9431-39d4f035ae4e)
![Screen Shot 2025-01-11 at 4 55 46 PM](https://github.com/user-attachments/assets/3cb3f589-e5e3-43d9-bfff-360cdcf7176e)
