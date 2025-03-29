# Eshopper Django Backend

This is the Django REST Framework backend for the Eshopper Flutter application. It provides API endpoints for user authentication, product management, shopping cart, orders, and favorites.

## Features

- User authentication (register, login, social login)
- Password reset functionality
- Product catalog with categories
- Shopping cart management
- Order processing
- Favorites/wishlist
- Admin interface for managing products, orders, and users

## Setup

### Prerequisites

- Python 3.8+
- pip (Python package manager)
- Virtual environment (recommended)

### Installation

1. Create and activate a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

2. Install the required packages:

```bash
pip install -r requirements.txt
```

3. Set up the database:

```bash
python manage.py migrate
```

4. Create a superuser for admin access:

```bash
python manage.py createsuperuser
```

5. Load initial data (optional):

```bash
python manage.py loaddata initial_data.json
```

### Running the Server

Start the development server:

```bash
python manage.py runserver
```

The API will be available at http://localhost:8000/api/

The admin interface will be available at http://localhost:8000/admin/

## API Endpoints

### Authentication

- `POST /api/auth/registration/` - Register a new user
- `POST /api/auth/login/` - Login
- `POST /api/auth/logout/` - Logout
- `POST /api/auth/password/reset/` - Request password reset
- `POST /api/auth/password/reset/confirm/` - Confirm password reset
- `POST /api/token/` - Get JWT token
- `POST /api/token/refresh/` - Refresh JWT token

### Users

- `GET /api/users/me/` - Get current user profile
- `PUT /api/users/me/` - Update user profile

### Products

- `GET /api/products/` - List all products
- `GET /api/products/{slug}/` - Get product details
- `GET /api/products/categories/` - List all categories
- `GET /api/products/categories/{slug}/` - Get category details
- `GET /api/products/categories/{slug}/products/` - Get products in a category

### Cart

- `GET /api/orders/cart/` - Get user's cart
- `POST /api/orders/cart/add_item/` - Add item to cart
- `POST /api/orders/cart/remove_item/` - Remove item from cart
- `POST /api/orders/cart/update_item/` - Update item quantity
- `POST /api/orders/cart/clear/` - Clear cart

### Orders

- `GET /api/orders/orders/` - List user's orders
- `POST /api/orders/orders/` - Create a new order
- `GET /api/orders/orders/{id}/` - Get order details

### Favorites

- `GET /api/orders/favorites/` - List user's favorite products
- `POST /api/orders/favorites/` - Add a product to favorites
- `DELETE /api/orders/favorites/{id}/` - Remove a product from favorites
- `POST /api/orders/favorites/toggle/` - Toggle a product as favorite

## Environment Variables

The following environment variables can be set in the `.env` file:

- `SECRET_KEY` - Django secret key
- `DEBUG` - Debug mode (True/False)
- `ALLOWED_HOSTS` - Comma-separated list of allowed hosts
- `CORS_ALLOWED_ORIGINS` - Comma-separated list of allowed CORS origins

## License

This project is licensed under the MIT License.