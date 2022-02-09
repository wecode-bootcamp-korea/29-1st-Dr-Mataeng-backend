import json

from django.http      import JsonResponse
from django.views     import View

from users.utils      import login_decorator
from reviews.models   import Review
from products.models  import ProductColor

class ReviewView(View):
    @login_decorator
    def post(self, request, *args, **kwargs):
        try:
            data       = json.loads(request.body)
            user       = request.user
            product_id = kwargs['product_id']
            title      = data['title']
            content    = data['content']
            image_url  = data['image_url'].split(',')
            rating     = data['rating']
            order_size = data['order_size']

            if not ProductColor.objects.filter(
                id                        = product_id, 
                productoption__size__name = order_size
                ).exists():
                return JsonResponse({"message" : "INVALID PRODUCT OR SIZE"}, status=400)

            if int(rating) < 1 or int(rating) > 5:
                return JsonResponse({"message" : "INVALID RATING"}, status=400)

            review, is_created_flag = Review.objects.get_or_create(
                user_id          = user.id,
                product_color_id = product_id,
                title            = title,
                content          = content,
                image_url        = image_url,
                rating           = rating,
                order_size       = order_size,
                )
            review.save()
            return JsonResponse({"message" : "SUCCESS"}, status=201) 
        except KeyError:
            return JsonResponse({"message" : "KEY ERROR"}, status=400)
        except Exception as e:
            return JsonResponse({"message" : getattr(e,"message",str(e))}, status=400)