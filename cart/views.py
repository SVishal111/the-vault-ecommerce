from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from store.models import Product, Cart, CartItem
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required(login_url='login')
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.all()

    total = 0
    for item in items:
        total += item.product.price * item.quantity

    return render(request, 'cart/cart.html', {
        'cart': cart,
        'items': items,
        'total': total
    })



def add_to_cart(request, product_id):
    if not request.user.is_authenticated:
        messages.warning(request, "Login first to add items to cart.")
        return redirect(f'/accounts/login/?next=/cart/add/{id}/')
    product = get_object_or_404(Product, id=product_id)

    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        cart_item.quantity += 1
    cart_item.save()

    return redirect('cart_view')


@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()
    return redirect('cart_view')


@login_required
def increase_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.quantity += 1
    item.save()
    return redirect('cart_view')


@login_required
def decrease_quantity(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)

    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()

    return redirect('cart_view')
