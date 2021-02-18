from django import template
from Order.models import Order



register = template.Library()


@register.filter
def cart_count(user):
    order = Order.objects.filter(user = user,ordered=False)
    if order.exists():
        return order[0].orders_item.count()
    else:
        return 0