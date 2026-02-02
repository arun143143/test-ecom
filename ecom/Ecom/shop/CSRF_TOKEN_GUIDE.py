# CSRF TOKEN GUIDE FOR DJANGO POST REQUESTS
# This document explains CSRF protection and how to fix the 403 error

"""
========================================
WHAT IS CSRF? (Cross-Site Request Forgery)
========================================

CSRF is a security vulnerability where:
- An attacker tricks a user into submitting a form on another website
- The form performs unwanted actions on the original website
- Example: Delete products, transfer money, change passwords

Django CSRF PROTECTION:
- Generates unique token for each form
- Token must be sent with POST requests
- Server validates token before processing data
- Prevents unauthorized form submissions


========================================
ERROR: CSRF VERIFICATION FAILED (403)
========================================

ERROR MESSAGE:
"Forbidden (403) CSRF verification failed. Request aborted.
Reason: CSRF token missing."

CAUSES:
1. {% csrf_token %} missing from form template
2. Form not using POST method
3. Browser cookies disabled
4. Token not being sent with request


========================================
SOLUTION 1: ADD CSRF TOKEN TO HTML FORMS
========================================

INCORRECT (without CSRF token):
<form method="POST" action="/product/create/">
    <input type="text" name="name" required>
    <input type="number" name="price" required>
    <textarea name="description" required></textarea>
    <button type="submit">Create Product</button>
</form>

CORRECT (with CSRF token):
<form method="POST" action="/product/create/">
    {% csrf_token %}  <!-- ADD THIS LINE -->
    <input type="text" name="name" required>
    <input type="number" name="price" required>
    <textarea name="description" required></textarea>
    <button type="submit">Create Product</button>
</form>

WHAT {% csrf_token %} DOES:
- Generates hidden input field with name="csrfmiddlewaretoken"
- Contains unique token value
- Renders as: <input type="hidden" name="csrfmiddlewaretoken" value="...">
- Token sent with POST request to server
- Server validates token matches


========================================
SOLUTION 2: DJANGO FORM RENDERING
========================================

If using Django Forms (recommended):

CORRECT:
<form method="POST">
    {% csrf_token %}  <!-- REQUIRED -->
    {{ form.as_p }}  <!-- Renders all form fields -->
    <button type="submit">Save</button>
</form>

Django Form rendering options:
{{ form.as_p }}          <!-- Renders fields as <p> tags -->
{{ form.as_table }}      <!-- Renders as table rows -->
{{ form.as_ul }}         <!-- Renders as list items -->

MANUAL FIELD RENDERING:
<form method="POST">
    {% csrf_token %}
    <div>
        <label>Name:</label>
        {{ form.name }}
        {% if form.name.errors %}
            <span class="error">{{ form.name.errors }}</span>
        {% endif %}
    </div>
    <button type="submit">Save</button>
</form>


========================================
SOLUTION 3: AJAX POST REQUESTS
========================================

For JavaScript AJAX requests, add CSRF token to headers:

METHOD 1: Using Fetch API
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

fetch('/product/create/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrftoken  <!-- ADD TOKEN TO HEADER -->
    },
    body: JSON.stringify({
        name: 'Samsung Galaxy S21',
        price: 899.99,
        description: 'High quality smartphone',
        stock: 50,
        Category: 1
    })
})
.then(response => response.json())
.then(data => console.log(data));


METHOD 2: Using jQuery
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});

$.post('/product/create/', {
    name: 'Samsung Galaxy S21',
    price: 899.99,
    description: 'High quality smartphone',
    stock: 50,
    Category: 1
});


========================================
SOLUTION 4: CHECK DJANGO SETTINGS
========================================

Make sure middleware is enabled in settings.py:

CORRECT settings.py:
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',  <!-- REQUIRED -->
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CSRF SETTINGS:
CSRF_COOKIE_SECURE = False  # Set to True in production with HTTPS
CSRF_COOKIE_HTTPONLY = False  # JavaScript needs to read it for AJAX
CSRF_TRUSTED_ORIGINS = []  # Add trusted domains if needed


========================================
COMPLETE WORKING EXAMPLE
========================================

views.py:
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    
    # Pass both request and context to template
    return render(request, 'shop/product/product_form.html', {'form': form})


product_form.html:
{% extends 'shop/base.html' %}

{% block content %}
<div class="form-container">
    <h1>Create Product</h1>
    
    <!-- FORM WITH CSRF TOKEN -->
    <form method="POST" action="/product/create/">
        {% csrf_token %}  <!-- THIS IS REQUIRED -->
        
        <!-- Render form fields -->
        <div class="form-group">
            <label>Name:</label>
            {{ form.name }}
            {% if form.name.errors %}
                <span class="error">{{ form.name.errors }}</span>
            {% endif %}
        </div>
        
        <div class="form-group">
            <label>Price:</label>
            {{ form.price }}
            {% if form.price.errors %}
                <span class="error">{{ form.price.errors }}</span>
            {% endif %}
        </div>
        
        <div class="form-group">
            <label>Description:</label>
            {{ form.description }}
            {% if form.description.errors %}
                <span class="error">{{ form.description.errors }}</span>
            {% endif %}
        </div>
        
        <div class="form-group">
            <label>Stock:</label>
            {{ form.stock }}
            {% if form.stock.errors %}
                <span class="error">{{ form.stock.errors }}</span>
            {% endif %}
        </div>
        
        <div class="form-group">
            <label>Category:</label>
            {{ form.Category }}
            {% if form.Category.errors %}
                <span class="error">{{ form.Category.errors }}</span>
            {% endif %}
        </div>
        
        <button type="submit">Create Product</button>
    </form>
</div>
{% endblock %}


========================================
DEBUGGING CSRF ISSUES
========================================

STEP 1: Check if CSRF token in HTML
- Right-click form → Inspect Element
- Look for: <input type="hidden" name="csrfmiddlewaretoken">
- If missing → Add {% csrf_token %} to template

STEP 2: Check if cookies enabled
- Browser → Settings → Cookies
- Ensure cookies are enabled
- Clear browser cache and try again

STEP 3: Check if form method is POST
- Form must have: method="POST"
- GET requests don't need CSRF token
- Example: <form method="POST">

STEP 4: Check middleware
- Open settings.py
- Verify CsrfViewMiddleware is in MIDDLEWARE list
- Order matters! Should be after SessionMiddleware

STEP 5: Check DEBUG mode
- If DEBUG=False, check ALLOWED_HOSTS
- Add your domain to ALLOWED_HOSTS
- Example: ALLOWED_HOSTS = ['localhost', '127.0.0.1']


========================================
COMMON CSRF ERRORS AND FIXES
========================================

ERROR 1: CSRF token missing
Reason: {% csrf_token %} not in form
Fix: Add {% csrf_token %} to form template

ERROR 2: CSRF token incorrect
Reason: Token expired or mismatched
Fix: Reload page and get new token

ERROR 3: CSRF cookie not set
Reason: Session not created
Fix: Ensure SessionMiddleware is enabled

ERROR 4: CSRF header invalid
Reason: X-CSRFToken header not sent
Fix: Add X-CSRFToken to fetch/AJAX headers


========================================
CSRF TOKEN FLOW DIAGRAM
========================================

1. USER VISITS FORM PAGE (GET):
   Browser sends GET request
   ↓
   Server renders template with {% csrf_token %}
   ↓
   {% csrf_token %} generates unique token
   ↓
   Token embedded in HTML as hidden input
   ↓
   Browser receives HTML with token
   ↓
   Server also stores token in cookie

2. USER SUBMITS FORM (POST):
   Form submitted with hidden token field
   ↓
   Browser sends POST request with:
   - Form data
   - csrfmiddlewaretoken value
   - Cookie with same token
   ↓
   Server receives request
   ↓
   Server validates:
   - Token in POST data
   - Token in cookie
   - Both match
   ↓
   If valid → Process request
   If invalid → Return 403 Forbidden


========================================
BEST PRACTICES
========================================

✓ DO:
- Always use {% csrf_token %} in POST forms
- Store token in proper Django template
- Use Django Forms for automatic token handling
- Test forms locally before deployment
- Enable HTTPS in production
- Set CSRF_COOKIE_SECURE = True in production

✗ DON'T:
- Disable CSRF protection entirely
- Store CSRF token in database
- Share token between users
- Use GET for form submissions
- Ignore CSRF warnings


========================================
REFERENCES
========================================

Django CSRF Documentation:
https://docs.djangoproject.com/en/stable/ref/csrf/

CSRF Protection Overview:
https://owasp.org/www-community/attacks/csrf

More Information:
- Enable verbose error pages in DEBUG mode
- Check browser console for error details
- Use Django debug toolbar for debugging
"""
