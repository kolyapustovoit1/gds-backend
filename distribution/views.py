from django.shortcuts import get_object_or_404, redirect, render
from addorders.models import Order  # або адаптуй, якщо імпортується по-іншому
from django.contrib import messages

import pandas as pd


def index(request):
    recent_orders = Order.objects.order_by('-created_at')[:10]
    return render(request, 'distribution/index.html', {'recent_orders': recent_orders}) 


def all_orders(request):
    orders = Order.objects.order_by('-created_at')
    return render(request, 'distribution/orders.html', {'orders': orders})


def delete_order(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Order, pk=order_id)
        order.delete()
        messages.success(request, 'Замовлення успішно видалено.')
    return redirect('orders')


def distribute_order(request, order_id):
    order = get_object_or_404(Order, pk=order_id)

    file_path = order.file.path
    try:
        df = pd.read_excel(file_path)
        df = df[df['Кількість'] > 0]

        # Замість borders — orders
        orders = df.to_dict(orient='records')

        messages.success(request, f"Замовлення {order.product_name} успішно завантажено.")
    except Exception as e:
        messages.error(request, f"Помилка при завантаженні Excel: {e}")
        orders = []

    context = {
        'order': order,
        'orders': orders,
        'order_id': order.id,
    }

    return render(request, 'distribution/distribution.html', context)