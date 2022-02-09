import uuid

from django.views     import View
from django.http      import JsonResponse
from django.db        import transaction
from django.db.models import Sum,F

from users.utils      import login_decorator
from orders.models    import Order, OrderItem, OrderStatus
from carts.models     import Cart

class OrderView(View):
    @login_decorator
    def get(self, request, *args, **kwargs):
        try:
            user        = request.user
            orders      = Order.objects.filter(user=user)
            order_items = OrderItem.objects.filter(order__in=orders)
            total_price = order_items.aggregate\
                          (total_price=Sum(F('product_option__product_color__product__price') * F('quantity')))\
                          ['total_price']

            order_item_list = [{
                'order_item_id' : order_item.id,
                'product_id'    : order_item.product_option.product_color.id,
                'product_name'  : order_item.product_option.product_color.product.name,
                'product_image' : order_item.product_option.product_color.products_images.first().image_url,
                'product_color' : order_item.product_option.product_color.color.name,
                'product_size'  : order_item.product_option.size.name,
                'quantity'      : order_item.quantity,
                'price'         : int(order_item.product_option.product_color.product.price * order_item.quantity),
                'created_at'    : order_item.created_at,
                'updated_at'    : order_item.updated_at,
            }for order_item in order_items]

            order_list = [{
                'order_id'     : order.id,
                'user'         : user.name,
                'order_items'  : order_item_list,
                'total_price'  : int(total_price),
                'order_status' : order.order_status.status,
            }for order in orders]
            return JsonResponse({"result" : order_list}, status=200)
        except Exception as e:
            return JsonResponse({"message" : getattr(e,"message",str(e))}, status=400)