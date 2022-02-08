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

            with transaction.atomic():
                order_number = uuid.uuid4()

                # order = Order.objects.create(
                #     user_id         = user.id,
                #     order_number    = order_number,
                #     order_status_id = 

                # )

                order_item = OrderItem.objects.create(
                    
                )
                

        except:
            pass

    @LoginConfirm.login_decorator
    def delete(self, request, *args, **kwargs):
        try:
            pass
        except:
            pass