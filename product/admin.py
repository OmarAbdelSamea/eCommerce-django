from django.contrib import admin

from product.models import *


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Profile)
admin.site.register(Transaction)
admin.site.register(Share)
admin.site.register(Order)
admin.site.register(Gift)

