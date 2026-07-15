# Django E-Commerce REST API

A simple E-Commerce Backend API built using **Django REST Framework (DRF)**.

## Features

- JWT Authentication
- User Registration & Login
- Buyer & Seller Roles
- Product CRUD
- Category CRUD
- Seller Ownership Permissions
- Shopping Cart
- Cart Items
- Checkout System
- Order Management
- Search Products
- Filter Products
- Order Products
- Stock Management

---

## Technologies Used

- Python
- Django
- Django REST Framework
- MySQL
- Simple JWT
- Django Filter

---

## Installation

### Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
```

Go into the project directory

```bash
cd YOUR_REPOSITORY
```

Create a virtual environment

```bash
python -m venv venv
```

Activate it

### Windows

```bash
venv\Scripts\activate
```

### macOS/Linux

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run migrations

```bash
python manage.py migrate
```

Create a superuser

```bash
python manage.py createsuperuser
```

Run the server

```bash
python manage.py runserver
```

---

## API Endpoints

| Method | Endpoint   | Description             |
| ------ | ---------- | ----------------------- |
| POST   | /register/ | Register User           |
| POST   | /login/    | Login User              |
| GET    | /product/  | View Products           |
| POST   | /product/  | Create Product (Seller) |
| GET    | /category/ | View Categories         |
| POST   | /category/ | Create Category (Admin) |
| GET    | /cart/     | View Cart               |
| POST   | /cart/     | Create Cart             |
| GET    | /cartitem/ | View Cart Items         |
| POST   | /cartitem/ | Add Product to Cart     |
| POST   | /checkout/ | Checkout                |
| GET    | /order/    | View Orders             |

---

## Authentication

This project uses **JWT Authentication**.

After logging in, include your access token in requests.

```
Authorization: Bearer YOUR_ACCESS_TOKEN
```

---

## User Roles

### Buyer

- View Products
- Create Cart
- Add Products to Cart
- Checkout
- View Orders

### Seller

- Create Products
- Update Own Products
- Delete Own Products

### Admin

- Manage Categories

---

## Author

Mandip Karki

Backend Developer | Python | Django | Django REST Framework
