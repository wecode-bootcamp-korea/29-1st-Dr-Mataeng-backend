import uuid

from datetime import datetime

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
                'created_at'    : order_item.created_at.strftime("%Y년 %m월 %d일 %H:%M"),
                'updated_at'    : order_item.created_at.strftime("%Y년 %m월 %d일 %H:%M"),
            }for order_item in order_items]

            order_list = [{
                'order_id'     : order.id,
                'order_number' : order.order_number,
                'user'         : user.name,
                'order_items'  : order_item_list,
                'total_price'  : int(total_price),
                'order_status' : order.order_status.status,
            }for order in orders]
            return JsonResponse({"result" : order_list}, status=200)
        except Exception as e:
            return JsonResponse({"message" : getattr(e,"message",str(e))}, status=400)
            
    @login_decorator
    def post(self, request, *args, **kwargs):
        try:
            user        = request.user
            cart_ids    = request.GET.getlist("cart_id")
            carts       = Cart.objects.filter(id__in=cart_ids, user=user)

            if not carts.exists():
                return JsonResponse({"message" : "NOT EXIST CARTS"}, status=400)

            total_price = carts.aggregate\
                          (total_price=Sum(F('product_option__product_color__product__price') * F('quantity')))\
                          ['total_price']

            with transaction.atomic():
                order_number = uuid.uuid4()
                order_status = OrderStatus.objects.get(status="결제완료")

                order = Order.objects.create(
                    user         = user,
                    order_number = order_number,
                    order_status = order_status,
                )

                order_items = [OrderItem(
                    order          = order,
                    product_option = cart.product_option,
                    quantity       = cart.quantity
                ) for cart in carts]

                if user.point < total_price:
                    return JsonResponse({"message" : "NOT ENOUGH POINT"}, status=400)

                user.point -= total_price
                user.save()

                carts.delete()

                OrderItem.objects.bulk_create(order_items)
            return JsonResponse({"message" : "SUCCESS"}, status=201)
        except Exception as e:
            return JsonResponse({"message" : getattr(e,"message",str(e))}, status=400)