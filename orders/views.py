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