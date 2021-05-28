from django.forms import ModelChoiceField, ModelForm
from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *
from .utils import ImageValidationMixin


class SmartphoneAdminForm(ModelForm, ImageValidationMixin):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].help_text = mark_safe(
            """<span style="color:red; font-size:14px;">If resolution of the uploaded image is more than {}x{}, 
            it will be cropped</span>""".format(*Product.MAX_RESOLUTION)
        )
        instance = kwargs.get('instance')
        if instance and not instance.sd:
            self.fields['sd_memory_max'].widget.attrs.update({
                'readonly': True, 'style': 'background: lightgrey'
            })

    def clean(self):
        if not self.cleaned_data['sd']:
            self.cleaned_data['sd_memory_max'] = None
        return self.cleaned_data

    def clean_image(self):
        return self.validate_image()


class NotebookAdminForm(ModelForm, ImageValidationMixin):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].help_text = mark_safe(
            """<span style="color:red; font-size:14px;">If the resolution of the uploaded image is more than {}x{}, 
            it will be cropped</span>""".format(*Product.MAX_RESOLUTION)
        )

    def clean_image(self):
        return self.validate_image()


class NotebookAdmin(admin.ModelAdmin):
    form = NotebookAdminForm
    prepopulated_fields = {'slug': ('title',)}

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='notebooks'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class SmartphoneAdmin(admin.ModelAdmin):
    change_form_template = 'admin.html'
    form = SmartphoneAdminForm
    prepopulated_fields = {'slug': ('title',)}

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='smartphones'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Category)
admin.site.register(Notebook, NotebookAdmin)
admin.site.register(Smartphone, SmartphoneAdmin)
admin.site.register(CartProduct)
admin.site.register(Cart1)
admin.site.register(Customer)


