from django.db import models


class CategorySpecification(models.Model):
    """
    Specification of concrete category
    """
    category = models.ForeignKey('mainapp.Category', verbose_name='category', on_delete=models.CASCADE)
    spec_name = models.CharField(max_length=100, verbose_name='Specification name')
    spec_filter_name = models.CharField(max_length=50, verbose_name='Name for filter')
    unit_of_measure = models.CharField(max_length=50, verbose_name='Unit of measure', null=True, blank=True)

    class Meta:
        unique_together = ('category', 'spec_name', 'spec_filter_name')

    def __str__(self):
        return f'{self.category.name} | {self.spec_name}'


class SpecificationValidator(models.Model):
    """
    Validator for values of concrete specification belonging to concrete category
    """
    category = models.ForeignKey('mainapp.Category', verbose_name='category', on_delete=models.CASCADE)
    spec_key = models.ForeignKey(CategorySpecification, verbose_name='Specification key', on_delete=models.CASCADE)
    valid_spec_value = models.CharField(max_length=100, verbose_name='Valid value')

    def __str__(self):
        return f'Category "{self.category.name}" | ' \
               f'Specification "{self.spec_key.spec_name}" | ' \
               f'Valid value "{self.valid_spec_value}"'


class ProductSpecifications(models.Model):
    """
    Product specifications
    """
    product = models.ForeignKey('mainapp.Product', verbose_name='Product', on_delete=models.CASCADE)
    spec = models.ForeignKey(CategorySpecification, verbose_name='Specification', on_delete=models.CASCADE)
    value = models.CharField(max_length=255, verbose_name='Value')

    def __str__(self):
        return f'Product "{self.product.title}" | ' \
               f'Specification "{self.spec.spec_name}" | ' \
               f'Value - {self.value}'

