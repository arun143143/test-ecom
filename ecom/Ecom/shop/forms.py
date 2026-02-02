from django import forms
from django.contrib.auth.models import User
from .models import Products, Category, Order, Customer

# ========================================
# USER FORM
# ========================================
class UserForm(forms.ModelForm):
    # Custom password field not in model
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    
    class Meta:
        model = User  # Maps to Django's User model
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            # TextInput renders as <input type="text">
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            # EmailInput renders as <input type="email">
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }


# ========================================
# CUSTOMER FORM
# ========================================
class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer  # Maps to Customer model
        # These fields will be rendered in HTML form
        fields = ['phone', 'address', 'city', 'state', 'postal_code', 'country']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            # Textarea renders as <textarea>
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
        }


# ========================================
# PRODUCT FORM
# ========================================
class ProductForm(forms.ModelForm):
    """
    Form for creating and updating products
    
    PAYLOAD STRUCTURE (POST data expected):
    {
        'name': 'Product Name',           # Required, max 100 chars, unique
        'price': '99.99',                 # Required, decimal with 2 places
        'description': 'Product desc',    # Required, text field
        'stock': '50',                    # Required, integer value
        'Category': '1'                   # Required, category ID (foreign key)
    }
    """
    class Meta:
        model = Products  # Maps to Products model
        # These fields define what data is expected in POST request
        fields = ['name', 'price', 'description', 'stock', 'Category']
        widgets = {
            # TextInput renders as <input type="text">
            # Used for short string inputs like product name
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            # NumberInput renders as <input type="number">
            # step='0.01' allows decimal values (99.99)
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            # Textarea renders as <textarea>
            # rows=4 sets height to 4 lines
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            # NumberInput for integers
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            # Select renders as <select> dropdown
            # Automatically populated with Category choices from database
            'Category': forms.Select(attrs={'class': 'form-control'}),
        }


# ========================================
# CATEGORY FORM
# ========================================
class CategoryForm(forms.ModelForm):
    """
    Form for creating and updating categories
    
    PAYLOAD STRUCTURE (POST data expected):
    {
        'name': 'Category Name',          # Required, max 100 chars, unique
        'description': 'Category desc'    # Required, text field
    }
    """
    class Meta:
        model = Category  # Maps to Category model
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


# ========================================
# ORDER FORM
# ========================================
class OrderForm(forms.ModelForm):
    """
    Form for updating order status
    
    PAYLOAD STRUCTURE (POST data expected):
    {
        'status': 'pending'  # Choice: pending, processing, shipped, delivered
    }
    """
    class Meta:
        model = Order  # Maps to Order model
        fields = ['status']
        widgets = {
            # Select renders as <select> dropdown
            # Automatically populated with status choices defined in model
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

