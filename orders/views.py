from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from store.models import Cart, CartItem, Order, OrderItem


@login_required
def checkout(request):
    cart = Cart.objects.get(user=request.user)
    items = cart.items.all()

    if not items:
        return redirect('cart_view')

    total = 0
    for item in items:
        total += item.product.price * item.quantity

    # Create Order
    order = Order.objects.create(
        user=request.user,
        total_price=total
    )

    # Create Order Items
    for item in items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )

        # Reduce stock
        item.product.stock -= item.quantity
        item.product.save()

    # Clear Cart
    items.delete()

    return redirect('order_history')

@login_required
def order_history(request):
    orders = request.user.orders.all().order_by('-created_at')
    return render(request, 'orders/history.html', {'orders': orders})