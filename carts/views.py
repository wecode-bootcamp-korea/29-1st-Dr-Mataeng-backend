import json

from django.http      import JsonResponse
from django.views     import View

from users.utils      import LoginConfirm
from carts.models     import Cart
from products.models  import ProductOption

class CartView(View):
    @LoginConfirm.login_decorator
    def get(self, request, *args, **kwargs):
        try:
            user  = request.user
            carts = Cart.objects.filter(user=user)

            data = [{
                'cart_id'       : cart.id,
                'product_id'    : cart.product_option.product_color.id,
                'product_name'  : cart.product_option.product_color.product.name,
                'product_image' : cart.product_option.product_color.products_images.first().image_url,
                'product_color' : cart.product_option.product_color.color.name,
                'product_size'  : cart.product_option.size.name,
                'quantity'      : cart.quantity,
                'price'         : int(cart.product_option.product_color.product.price * cart.quantity)
            }for cart in carts]
            return JsonResponse({"result" : data}, status=200)
        except Exception as e:
            return JsonResponse({"message" : getattr(e,"message",str(e))}, status=400)