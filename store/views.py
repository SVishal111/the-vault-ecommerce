from django.shortcuts import render

from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from .models import Product, Order
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.contrib.auth import login
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Sum

def is_admin(user):
    return user.is_staff

@login_required
def redirect_after_login(request):
    if request.user.is_staff:
        return redirect('admin_dashboard')
    else:
        return redirect('product_list')

@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):

    total_users = User.objects.count()
    total_products = Product.objects.count()
    total_orders = Order.objects.count()

    total_revenue = Order.objects.filter(
        status='Delivered'
    ).aggregate(Sum('total_price'))['total_price__sum'] or 0

    recent_orders = Order.objects.order_by('-created_at')[:5]
    recent_users = User.objects.order_by('-date_joined')[:5]

    context = {
        'total_users': total_users,
        'total_products': total_products,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'recent_orders': recent_orders,
        'recent_users': recent_users,
    }

    return render(request, 'admin/dashboard.html', context)


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('product_list')
    else:
        form = UserCreationForm()

    return render(request, "registration/register.html", {'form': form})

def product_list(request):
    products = Product.objects.filter(is_available=True)
    categories = Category.objects.all()

    # Filter by category
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category__id=category_id)

    # Search
    search_query = request.GET.get('search')
    if search_query:
        products = products.filter(name__icontains=search_query)

    context = {
        'products': products,
        'categories': categories
    }
    return render(request, 'store/product_list.html', context)


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'store/product_detail.html', {'product': product})
