from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required
from django.http import JsonResponse
from .models import Product
from .forms import ProductForm

# Utility Function
def admin_required(user):
    """Check if user is an admin."""
    return user.is_staff

# Public Views
def index(request):
    """Home Page / Index View."""
    return render(request, 'index.html')

def signup(request):
    """Signup View."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, 'Signup successful!')
            return redirect('index')
        else:
            messages.error(request, 'Signup failed. Please correct the errors below.')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login(request):
    """Login View."""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('index')
        else:
            messages.error(request, 'Invalid login details.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout(request):
    """Logout View."""
    auth_logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('index')

@login_required
def profile(request):
    """Profile View."""
    return render(request, 'profile.html', {'user': request.user})

def cart(request):
    """Cart View."""
    cart = request.session.get('cart', {})
    return render(request, 'cart.html', {'cart': cart})

def add_to_cart(request):
    """Add to Cart View."""
    product_id = request.POST.get('product_id')
    cart = request.session.get('cart', {})
    if product_id:
        cart[product_id] = cart.get(product_id, 0) + 1
        request.session['cart'] = cart
        messages.success(request, 'Product added to cart.')
    return redirect('product_list')

def remove_from_cart(request):
    """Remove from Cart View."""
    product_id = request.POST.get('product_id')
    cart = request.session.get('cart', {})
    if product_id in cart:
        del cart[product_id]
        request.session['cart'] = cart
        messages.success(request, 'Product removed from cart.')
    return redirect('cart')

def update_cart(request):
    """Update Cart View."""
    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity', 1))
    cart = request.session.get('cart', {})
    if product_id in cart and quantity > 0:
        cart[product_id] = quantity
        request.session['cart'] = cart
        messages.success(request, 'Cart updated successfully.')
    elif product_id in cart and quantity <= 0:
        del cart[product_id]
        messages.success(request, 'Product removed from cart.')
    request.session['cart'] = cart
    return redirect('cart')

def get_cart(request):
    """Get Cart View."""
    cart = request.session.get('cart', {})
    products = []
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, pk=product_id)
        products.append({
            'product': product,
            'quantity': quantity,
        })
    return render(request, 'cart_detail.html', {'cart': products})

def checkout_view(request):
    """Checkout View."""
    cart = request.session.get('cart', {})
    products = []
    total_price = 0
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, pk=product_id)
        products.append({
            'product': product,
            'quantity': quantity,
            'total': product.price * quantity
        })
        total_price += product.price * quantity
    
    if request.method == 'POST':
        return redirect('place_order')  # Redirect to the order placement after checkout

    return render(request, 'checkout.html', {'cart': products, 'total_price': total_price})

def place_order(request):
    """Place Order View."""
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, 'Your cart is empty. Add products to proceed.')
        return redirect('product_list')

    # Sample code to handle order processing
    order_details = []
    total_price = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, pk=product_id)
        order_details.append(f"{product.name} (x{quantity}) - ${product.price * quantity}")
        total_price += product.price * quantity
        # Logic to reduce stock or any other order processing can be done here

    # Clear the cart after order processing
    request.session['cart'] = {}
    messages.success(request, 'Your order has been placed successfully!')
    
    # Assuming the order ID is 1 for this example; replace with actual order logic
    return redirect('order_confirmation', order_id=1)

def order_confirmation_view(request, order_id):
    """Order Confirmation View."""
    # Replace with actual order retrieval logic based on the order_id
    order_details = [
        {"name": "Sample Product 1", "quantity": 2, "price": 10},
        {"name": "Sample Product 2", "quantity": 1, "price": 20},
    ]
    total_price = sum(item["quantity"] * item["price"] for item in order_details)

    return render(request, 'order_confirmation.html', {
        'order_id': order_id,
        'order_details': order_details,
        'total_price': total_price
    })

def some_view(request):
    """Some View."""
    # Logic for this view goes here. For example, it could be a simple page.
    return render(request, 'some_page.html')

def is_logged_in(request):
    """Check if the user is logged in."""
    is_authenticated = request.user.is_authenticated
    return JsonResponse({'is_logged_in': is_authenticated})

# Product Views for All Users
def product_list(request):
    """Product List View (Read)."""
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

def product_detail(request, pk):
    """Product Detail View."""
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product.html', {'product': product})

# Product Management Views (Admin Only)
@user_passes_test(admin_required)
def product_create(request):
    """Create Product."""
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product created successfully.')
            return redirect('product_list')
        else:
            messages.error(request, 'Failed to create product. Please correct the errors below.')
    else:
        form = ProductForm()
    return render(request, 'product_form.html', {'form': form})

@user_passes_test(admin_required)
def product_update(request, pk):
    """Update Product."""
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully.')
            return redirect('product_list')
        else:
            messages.error(request, 'Failed to update product. Please correct the errors below.')
    else:
        form = ProductForm(instance=product)
    return render(request, 'product_form.html', {'form': form})

@user_passes_test(admin_required)
def product_delete(request, pk):
    """Delete Product."""
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully.')
        return redirect('product_list')
    return render(request, 'product_confirm_delete.html', {'product': product})
