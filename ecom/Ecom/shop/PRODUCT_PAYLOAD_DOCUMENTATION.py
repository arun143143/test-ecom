# PRODUCT POST METHOD PAYLOAD DOCUMENTATION
# This file explains the payload structure for creating and updating products

"""
========================================
1. CREATE PRODUCT - POST REQUEST PAYLOAD
========================================

URL: /product/create/
METHOD: POST
Content-Type: application/x-www-form-urlencoded OR multipart/form-data

PAYLOAD FIELDS (Form Data):
----------------------------

Field Name: name
Type: String
Max Length: 100
Required: YES
Example Value: "Samsung Galaxy S21"
Description: Product name - must be unique

Field Name: price
Type: Decimal
Max Digits: 10
Decimal Places: 2
Required: YES
Example Value: "899.99"
Description: Product price (e.g., 99.99)

Field Name: description
Type: Text (Long String)
Required: YES
Example Value: "High-quality smartphone with amazing features..."
Description: Detailed product description

Field Name: stock
Type: Integer
Required: YES
Default Value: 0
Example Value: "50"
Description: Quantity available in stock

Field Name: Category
Type: Integer (Foreign Key)
Required: YES
Example Value: "1"
Description: Category ID (must exist in database)

----------------------------
EXAMPLE 1: CREATE NEW PRODUCT
----------------------------

HTML FORM:
<form method="POST" action="/product/create/">
    {% csrf_token %}
    <input type="text" name="name" placeholder="Product Name" required>
    <input type="number" name="price" step="0.01" placeholder="Price" required>
    <textarea name="description" placeholder="Description" required></textarea>
    <input type="number" name="stock" placeholder="Stock" required>
    <select name="Category" required>
        <option value="">Select Category</option>
        <option value="1">Electronics</option>
        <option value="2">Clothing</option>
    </select>
    <button type="submit">Create Product</button>
</form>

⚠️ IMPORTANT: {% csrf_token %} is REQUIRED for POST requests
This generates a hidden input with CSRF token to prevent security attacks
Without it, you'll get: Forbidden (403) - CSRF verification failed

FORM DATA (URL ENCODED):
name=Samsung+Galaxy+S21&price=899.99&description=High+quality+smartphone&stock=50&Category=1

CURL REQUEST:
curl -X POST http://localhost:8000/product/create/ \
  -d "name=Samsung Galaxy S21" \
  -d "price=899.99" \
  -d "description=High quality smartphone" \
  -d "stock=50" \
  -d "Category=1"

PYTHON REQUESTS EXAMPLE:
import requests

payload = {
    'name': 'Samsung Galaxy S21',
    'price': '899.99',
    'description': 'High quality smartphone with amazing features',
    'stock': '50',
    'Category': '1'
}

response = requests.post('http://localhost:8000/product/create/', data=payload)
print(response.status_code)  # 302 (redirect on success)


========================================
2. UPDATE PRODUCT - POST REQUEST PAYLOAD
========================================

URL: /product/<id>/update/
METHOD: POST
Content-Type: application/x-www-form-urlencoded

SAME FIELDS AS CREATE (all optional if already filled):

EXAMPLE: UPDATE PRODUCT WITH ID=5

HTML FORM:
<form method="POST" action="/product/5/update/">
    {% csrf_token %}
    <input type="text" name="name" value="Samsung Galaxy S21" required>
    <input type="number" name="price" step="0.01" value="899.99" required>
    <textarea name="description" required>High quality smartphone</textarea>
    <input type="number" name="stock" value="50" required>
    <select name="Category" required>
        <option value="1" selected>Electronics</option>
    </select>
    <button type="submit">Update Product</button>
</form>

CURL REQUEST:
curl -X POST http://localhost:8000/product/5/update/ \
  -d "name=Samsung Galaxy S21 Ultra" \
  -d "price=1099.99" \
  -d "description=Updated description" \
  -d "stock=100" \
  -d "Category=1"

PYTHON REQUESTS EXAMPLE:
payload = {
    'name': 'Samsung Galaxy S21 Ultra',
    'price': '1099.99',
    'description': 'Updated description with more details',
    'stock': '100',
    'Category': '1'
}

response = requests.post('http://localhost:8000/product/5/update/', data=payload)


========================================
3. VALIDATION RULES (Django ORM)
========================================

NAME Field:
- Length: 1-100 characters
- Unique: YES (cannot duplicate)
- Cannot be empty
- Error: "Product with this name already exists"

PRICE Field:
- Decimal with 2 decimal places
- Must be positive number
- Example valid: 99.99, 10.50, 1000.00
- Example invalid: 99.9, -50, abc

DESCRIPTION Field:
- Can be any length text
- Cannot be empty
- Supports HTML content (stored as-is)

STOCK Field:
- Integer only
- Default: 0
- Cannot be negative
- Example valid: 0, 50, 1000
- Example invalid: -5, 10.5, abc

CATEGORY Field:
- Must be existing Category ID
- Foreign key relationship
- Cannot be null
- Error if ID doesn't exist: "Invalid choice"


========================================
4. DJANGO ORM PROCESSING IN VIEWS
========================================

When POST data is received:

1. FORM VALIDATION:
   form = ProductForm(request.POST)
   if form.is_valid():
       # Django validates all fields against model requirements
       # Checks unique constraint on name
       # Checks data types and ranges
       
2. DATABASE SAVE:
   form.save()
   # Executes SQL INSERT or UPDATE:
   # INSERT: INSERT INTO shop_products (name, price, description, stock, Category_id) 
   #         VALUES ('Samsung Galaxy S21', 899.99, '...', 50, 1)
   # UPDATE: UPDATE shop_products SET name='...', price=... WHERE id=5
   
3. RESPONSE:
   redirect('product_list')
   # After save, redirects to product list view


========================================
5. COMMON VALIDATION ERRORS
========================================

Error 1: Name Already Exists
Form Data: {name: "Samsung Galaxy S21"}
Error: "Product with this name already exists"
Solution: Use a unique name or update existing product

Error 2: Price Format Invalid
Form Data: {price: "99.9"}
Error: "Ensure that there are at most 2 decimal places."
Solution: Use format like 99.99

Error 3: Category Does Not Exist
Form Data: {Category: "999"}
Error: "Select a valid choice. 999 is not one of the available choices."
Solution: Use valid category ID from database

Error 4: Missing Required Field
Form Data: {name: "Product", price: "100"}
Error: "This field is required." (for description, stock, Category)
Solution: Provide all required fields

Error 5: Negative Stock
Form Data: {stock: "-50"}
May allow or reject depending on validation (currently allows)
Solution: Use positive numbers only


========================================
6. COMPLETE WORKING EXAMPLE
========================================

VIEW FUNCTION:
def product_create(request):
    if request.method == 'POST':
        # 1. Receive POST data
        form = ProductForm(request.POST)
        
        # 2. Validate data
        if form.is_valid():
            # 3. Save to database (INSERT)
            form.save()
            # 4. Redirect
            messages.success(request, 'Product created successfully!')
            return redirect('product_list')
    else:
        form = ProductForm()
    
    context = {'form': form, 'title': 'Create Product'}
    return render(request, 'shop/product/product_form.html', context)

WHAT HAPPENS:
1. GET request → Display empty form
2. POST request → Process form data
3. If valid → Insert into database → Redirect to list
4. If invalid → Display form with error messages


========================================
7. DATABASE SCHEMA REFERENCE
========================================

CREATE TABLE shop_products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    description TEXT NOT NULL,
    stock INTEGER DEFAULT 0,
    Category_id INTEGER NOT NULL,
    FOREIGN KEY (Category_id) REFERENCES shop_category(id)
);


========================================
8. TESTING THE PAYLOAD
========================================

Method 1: Using Django Shell
python manage.py shell
>>> from shop.models import Products, Category
>>> cat = Category.objects.get(id=1)
>>> p = Products.objects.create(
...     name='Test Product',
...     price=99.99,
...     description='Test description',
...     stock=10,
...     Category=cat
... )
>>> p.save()

Method 2: Using Admin Panel
1. Go to http://localhost:8000/admin/
2. Click "Products"
3. Click "Add Product"
4. Fill form and save

Method 3: Using Web Form
1. Go to http://localhost:8000/product/create/
2. Fill form with valid data
3. Submit

Method 4: Using Postman/curl
curl -X POST http://localhost:8000/product/create/ \
  -d "name=Test&price=99.99&description=Test&stock=10&Category=1"

"""
