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
                'product_like'  : cart.product_option.product_color.like_cnt,
                'product_color' : cart.product_option.product_color.color.name,
                'product_size'  : cart.product_option.size.name,
                'quantity'      : cart.quantity,
                'price'         : int(cart.product_option.product_color.product.price * cart.quantity)
            }for cart in carts]
            return JsonResponse({"result" : data}, status=200)
        except Exception as e:
            return JsonResponse({"message" : getattr(e,"message",str(e))}, status=400)

    @LoginConfirm.login_decorator
    def post(self, request, *args, **kwargs):
        try:
            data       = json.loads(request.body)
            user       = request.user
            product_id = data['product_id']
            size       = data['size']
            quantity   = int(data['quantity'])

            if not ProductOption.objects.filter(
                product_color_id = product_id, 
                size__name       = size
                ).exists():
                return JsonResponse({"message" : "PRODUCT OR SIZE DOSE NOT EXIST"}, status=400)

            product_option = ProductOption.objects.get(
                product_color_id = product_id,
                size__name       = size
                )

            if quantity > int(product_option.stock) or quantity < 1:
                return JsonResponse({"message" : "INVALID QUANTITY"}, status=400)

            cart, is_created_flag = Cart.objects.get_or_create(
                user_id        = user.id,
                product_option = product_option,
                quantity       = quantity
            )
            cart.save()
            return JsonResponse({"message" : "SUCCESS"}, status=201) 
        except KeyError:
            return JsonResponse({"message" : "KEY ERROR"}, status=400)
        except Exception as e:
            return JsonResponse({"message" : getattr(e,"message",str(e))}, status=400)

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