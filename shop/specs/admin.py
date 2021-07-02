from django.contrib import admin

from .models import *

admin.site.register(ProductSpecifications)
admin.site.register(CategorySpecification)
admin.site.register(SpecificationValidator)
