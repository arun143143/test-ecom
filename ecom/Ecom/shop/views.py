from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Products, Category, Order, Customer
from .forms import UserForm, CustomerForm, ProductForm, CategoryForm, OrderForm
from django.db.models import Q

# ========== HOME & PRODUCTS ==========
def home(request):
    # Get all products from database
    products = Products.objects.all()
    # Get all categories from database
    categories = Category.objects.all()
    # Check if user filtered by category
    category_id = request.GET.get('category')
    
    # If category filter is applied, filter products
    if category_id:
        products = products.filter(Category_id=category_id)
    
    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'shop/home.html', context)

def product_detail(request, id):
    # Get single product by id or return 404 if not found
    product = get_object_or_404(Products, id=id)
    context = {'product': product}
    return render(request, 'shop/product_detail.html', context)

def category_view(request, id):
    # Get single category by id
    category = get_object_or_404(Category, id=id)
    # Get all products in this category using filter
    products = Products.objects.filter(Category_id=id)
    context = {
        'category': category,
        'products': products,
    }
    return render(request, 'shop/category.html', context)

# ========== USER CRUD ==========

# READ - List all users
def user_list(request):
    # Get all users from database
    users = User.objects.all()
    context = {'users': users}
    return render(request, 'shop/user/user_list.html', context)

# READ - Get single user details
def user_detail(request, id):
    # Get single user by id
    user = get_object_or_404(User, id=id)
    # Try to get customer profile (one-to-one relationship)
    try:
        customer = user.customer_profile
    except:
        customer = None
    context = {
        'user': user,
        'customer': customer,
    }
    return render(request, 'shop/user/user_detail.html', context)

# CREATE - Create new user
def user_create(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        customer_form = CustomerForm(request.POST)
        
        if user_form.is_valid() and customer_form.is_valid():
            # Save user without committing to database
            user = user_form.save(commit=True)
            password = request.POST.get('password')
            
            # Set password using Django's set_password method (hashes the password)
            if password:
                user.set_password(password)
            else:
                user.set_password('default123')
            
            # Now save to database
            user.save()
            user.refresh_from_db()  # Load the customer_profile relation
        
            
            # Save customer profile linked to user
            customer = customer_form.save(commit=False)
            customer.user = user  # Set the foreign key relationship
            customer.save()
            customer.refresh_from_db()
            
            
            messages.success(request, 'User created successfully!')
            return redirect('user_detail', id=user.id)
    else:
        user_form = UserForm()
        customer_form = CustomerForm()
    
    context = {
        'user_form': user_form,
        'customer_form': customer_form,
        'title': 'Create User'
    }
    return render(request, 'shop/user/user_form.html', context)

# UPDATE - Update existing user
def user_update(request, id):
    # Get user by id
    user = get_object_or_404(User, id=id)
    # Get or create related customer profile
    try:
        customer = user.customer_profile
    except:
        customer = Customer.objects.create(user=user)
    
    if request.method == 'POST':
        # Pass instance to update existing record
        user_form = UserForm(request.POST, instance=user)
        customer_form = CustomerForm(request.POST, instance=customer)
        
        if user_form.is_valid() and customer_form.is_valid():
            # Save updates to database
            user = user_form.save()
            customer_form.save()
            messages.success(request, 'User updated successfully!')
            return redirect('user_detail', id=user.id)
    else:
        user_form = UserForm(instance=user)
        customer_form = CustomerForm(instance=customer)
    
    response = {
        'user_form': user_form,
        'customer_form': customer_form,
        'user': user,
        'title': 'Update User'
    }
    return render(request, 'shop/user/user_form.html', response)

# DELETE - Delete user
def user_delete(request, id):
    # Get user by id
    user = get_object_or_404(User, id=id)
    
    if request.method == 'DELETE':
        # Delete user from database
        user.delete()
        messages.success(request, 'User deleted successfully!')
        return redirect('user_list')
    
    context = {'user': user}
    return render(request, 'shop/user/user_confirm_delete.html', context)

# ========== CATEGORY CRUD ==========

# READ - List all categories
def category_list(request):
    # Get all categories from database
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'shop/category/category_list.html', context)

# CREATE - Create new category
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            # Save new category to database
            form.save()
            messages.success(request, 'Category created successfully!')
            return redirect('category_list')
    else:
        form = CategoryForm()
    
    context = {
        'form': form,
        'title': 'Create Category'
    }
    return render(request, 'shop/category/category_form.html', context)

# UPDATE - Update existing category
def category_update(request, id):
    # Get category by id
    category = get_object_or_404(Category, id=id)
    
    if request.method == 'POST':
        # Pass instance to update existing record
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            # Save updates to database
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    
    context = {
        'form': form,
        'category': category,
        'title': 'Update Category'
    }
    return render(request, 'shop/category/category_form.html', context)

# DELETE - Delete category
def category_delete(request, id):
    # Get category by id
    category = get_object_or_404(Category, id=id)
    
    if request.method == 'POST':
        # Delete category from database
        category.delete()
        messages.success(request, 'Category deleted successfully!')
        return redirect('category_list')
    
    context = {'category': category}
    return render(request, 'shop/category/category_confirm_delete.html', context)

# ========== PRODUCT CRUD ==========

# READ - List all products with search
def product_list(request):
    # Get all products from database
    products = Products.objects.all()
    # Check if search query exists
    search_query = request.GET.get('search')
    
    # If search query provided, filter products using Q objects
    if search_query:
        # Q object allows OR queries in Django
        products = products.filter(
            Q(name__icontains=search_query) | Q(description__icontains=search_query)
        )
    
    context = {'products': products, 'search_query': search_query}
    return render(request, 'shop/product/product_list.html', context)

# CREATE - Create new product
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            # Save new product to database
            form.save()
            messages.success(request, 'Product created successfully!')
            return redirect('product_list')
    else:
        form = ProductForm()
    
    context = {
        'form': form,
        'title': 'Create Product'
    }
    return render(request, 'shop/product/product_form.html', context)

# UPDATE - Update existing product
def product_update(request, id):
    # Get product by id
    product = get_object_or_404(Products, id=id)
    
    if request.method == 'POST':
        # Pass instance to update existing record
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            # Save updates to database
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    
    context = {
        'form': form,
        'product': product,
        'title': 'Update Product'
    }
    return render(request, 'shop/product/product_form.html', context)

# DELETE - Delete product
def product_delete(request, id):
    # Get product by id
    product = get_object_or_404(Products, id=id)
    
    if request.method == 'POST':
        # Delete product from database
        product.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('product_list')
    
    context = {'product': product}
    return render(request, 'shop/product/product_confirm_delete.html', context)

# ========== CART (Using Session) ==========

def add_to_cart(request, id):
    # Check if cart exists in session
    if 'cart' not in request.session:
        request.session['cart'] = {}
    
    cart = request.session['cart']
    # Get product by id
    product = get_object_or_404(Products, id=id)
    # Get quantity from request (default 1)
    quantity = int(request.GET.get('quantity', 1))
    
    # Check if product already in cart
    if str(id) in cart:
        # If yes, increase quantity
        cart[str(id)]['quantity'] += quantity
    else:
        # If no, add new product to cart
        cart[str(id)] = {
            'name': product.name,
            'price': str(product.price),
            'quantity': quantity,
        }
    
    # Mark session as modified to save changes
    request.session.modified = True
    messages.success(request, f'{product.name} added to cart!')
    return redirect('cart')

def cart_view(request):
    # Get cart from session
    cart = request.session.get('cart', {})
    total = 0
    items = []
    
    # Calculate totals
    for product_id, item in cart.items():
        item['total'] = float(item['price']) * item['quantity']
        total += item['total']
        items.append({'id': product_id, **item})
    
    context = {
        'items': items,
        'total': total,
    }
    return render(request, 'shop/cart.html', context)

def remove_from_cart(request, id):
    # Check if cart exists in session
    if 'cart' in request.session:
        cart = request.session['cart']
        # Check if product exists in cart
        if str(id) in cart:
            product_name = cart[str(id)]['name']
            # Remove product from cart
            del cart[str(id)]
            request.session.modified = True
            messages.success(request, f'{product_name} removed from cart!')
    return redirect('cart')

# ========== CHECKOUT & ORDERS ==========

@login_required(login_url='login')
def checkout(request):
    # Get cart from session
    cart = request.session.get('cart', {})
    
    # Check if cart is empty
    if not cart:
        messages.warning(request, 'Your cart is empty!')
        return redirect('home')
    
    # Calculate total
    total = 0
    for product_id, item in cart.items():
        total += float(item['price']) * item['quantity']
    
    if request.method == 'POST':
        # Get or create customer profile for current user
        try:
            customer = request.user.customer_profile
        except:
            customer = Customer.objects.create(user=request.user)
        
        # Update customer info from checkout form
        customer.phone = request.POST.get('phone', customer.phone)
        customer.address = request.POST.get('address', customer.address)
        customer.city = request.POST.get('city', customer.city)
        customer.state = request.POST.get('state', customer.state)
        customer.postal_code = request.POST.get('postal_code', customer.postal_code)
        customer.country = request.POST.get('country', customer.country)
        customer.save()
        
        # Create new order in database
        order = Order.objects.create(
            customer=customer,
            total_amount=total,
            status='pending'
        )
        
        # Add products to order and reduce stock
        for product_id in cart.keys():
            # Get product from database
            product = Products.objects.get(id=product_id)
            # Add product to order (many-to-many relationship)
            order.products.add(product)
            # Reduce stock based on quantity
            product.stock -= cart[str(product_id)]['quantity']
            # Save updated stock to database
            product.save()
        
        # Clear cart from session
        request.session['cart'] = {}
        request.session.modified = True
        
        messages.success(request, 'Order placed successfully!')
        return redirect('order_confirmation', order_id=order.id)
    
    # Get customer data for form pre-fill
    try:
        customer = request.user.customer_profile
    except:
        customer = None
    
    context = {
        'total': total,
        'cart_items': cart,
        'customer': customer,
    }
    return render(request, 'shop/checkout.html', context)

def order_confirmation(request, order_id):
    # Get order by id
    order = get_object_or_404(Order, id=order_id)
    context = {'order': order}
    return render(request, 'shop/order_confirmation.html', context)

@login_required(login_url='login')
def my_orders(request):
    # Get customer profile of logged-in user
    try:
        customer = request.user.customer_profile
        # Get all orders for this customer, ordered by creation date
        orders = customer.orders.all().order_by('-created_at')
    except:
        orders = []
    
    context = {'orders': orders}
    return render(request, 'shop/my_orders.html', context)

# ========== ORDERS MANAGEMENT ==========

# READ - List all orders with filtering
def order_list(request):
    # Get all orders from database, ordered by creation date
    orders = Order.objects.all().order_by('-created_at')
    # Check if status filter is applied
    status_filter = request.GET.get('status')
    
    # If status filter provided, filter orders
    if status_filter:
        orders = orders.filter(status=status_filter)
    
    context = {
        'orders': orders,
        'status_filter': status_filter,
        'status_choices': Order._meta.get_field('status').choices,
    }
    return render(request, 'shop/order/order_list.html', context)

# UPDATE - Update order status
def order_update_status(request, id):
    # Get order by id
    order = get_object_or_404(Order, id=id)
    
    if request.method == 'POST':
        # Pass instance to update existing order
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            # Save status update to database
            form.save()
            messages.success(request, f'Order #{order.id} status updated to {order.get_status_display()}!')
            return redirect('order_list')
    else:
        form = OrderForm(instance=order)
    
    context = {
        'form': form,
        'order': order,
        'title': f'Update Order #{order.id}'
    }
    return render(request, 'shop/order/order_form.html', context)

# READ - Get single order details
def order_detail(request, id):
    # Get order by id
    order = get_object_or_404(Order, id=id)
    context = {'order': order}
    return render(request, 'shop/order/order_detail.html', context)

# ========== AUTHENTICATION ==========

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        # Validate passwords match
        if password != confirm_password:
            messages.error(request, 'Passwords do not match!')
            return render(request, 'shop/register.html')
        
        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return render(request, 'shop/register.html')
        
        # Create new user (create_user hashes password automatically)
        user = User.objects.create_user(username=username, email=email, password=password)
        # Create customer profile for new user
        Customer.objects.create(user=user)
        
        messages.success(request, 'Account created successfully! Please login.')
        return redirect('login')
    
    return render(request, 'shop/register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authenticate user (checks username and password)
        user = authenticate(request, username=username, password=password)
        if user:
            # Log user in by creating session
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password!')
            return render(request, 'shop/login.html')
    
    return render(request, 'shop/login.html')

def logout_view(request):
    # Destroy user session
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('home')
