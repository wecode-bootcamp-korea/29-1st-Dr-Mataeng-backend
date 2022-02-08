import json

from django.http      import JsonResponse
from django.views     import View

from users.utils      import LoginConfirm
from carts.models     import Cart
from products.models  import ProductOption

class CartView(View):
    @LoginConfirm.login_decorator
    def delete(self, request, *args, **kwargs):
        try:
            user = request.user
            cart = Cart.objects.get(id=kwargs["cart_id"], user=user)

            cart.delete()
            return JsonResponse({"message" : "DELETE CART"}, status=200)
        except KeyError:
            return JsonResponse({"message" : "KEY ERROR"}, status=400)
        except Exception as e:
            return JsonResponse({"message" : getattr(e,"message",str(e))}, status=400)