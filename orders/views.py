import json
import uuid

from django.views   import View
from django.http    import JsonResponse
from django.db      import transaction
from orders.models import Order, OrderItem


from users.utils      import LoginConfirm
from carts.models     import Cart
from products.models  import ProductOption

class OrderView(View):
    @LoginConfirm.login_decorator
    def get(self, request, *args, **kwargs):
        try:
            pass
        except:
            pass

    @LoginConfirm.login_decorator
    def post(self, request, *args, **kwargs):
        try:
            data    = json.loads(request.body)
            user    = request.user
            cart_id = data["cart_id"]
            carts   = Cart.objects.filter(id=cart_id, user=user)

            total_price = carts.aggregate(total_price=Sum('product_option__product_color__product__price'))['total_price']

            with transaction.atomic():
                order_number = uuid.uuid4()

                # order = Order.objects.create(
                #     user_id         = user.id,
                #     order_number    = order_number,
                #     order_status_id = 

                # )

                order = Order.objects.create(
                    user = user,
                    ..
                )

                order_items = [OrderItem(
                    order    = order,
                    quantity = quantity,
                    ...
                )]

                OrderItem.objects.bulk_create(order_items)
                
                user.point -= total_price
                user.save()

        except:
            pass

    @LoginConfirm.login_decorator
    def delete(self, request, *args, **kwargs):
        try:
            pass
        except:
            pass
