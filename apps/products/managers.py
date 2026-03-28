from django.db import models


class CategoryQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)



class CategoryManager(models.Model):
    def get_queryset(self):
        return CategoryQuerySet(self.model, using=self._db).filter(is_deleted=False)

    def active(self):
        return self.get_queryset().active()
    

class BrandQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)



class BrandManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return BrandQuerySet(self.model, using=self._db).filter(is_deleted=False)

    def active(self):
        return self.get_queryset().active()


class ProductQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)

    def available(self):
        return self.active().filter(is_available=True)
    
    def featured(self):
        return self.available().filter(is_featured=True)

    def by_category_slug(self, slug):
        return self.available().filter(category__slug=slug)



class ProductManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return ProductManager(self.model, using=self._db).filter(is_deleted=False)

    def active(self):
        return self.get_queryset().active()
    def available(self):
        return self.get_queryset().available()
    
    def featured(self):
        return self.get_queryset().featured()