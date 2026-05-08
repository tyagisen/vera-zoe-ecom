from django.db import models

from decimal import Decimal

from django.core.exceptions import ValidationError
from django.utils.text import slugify
from apps.common.models import SoftDeleteModel, BaseModel
from apps.products.managers import CategoryManager, BrandManager, ProductManager
from .choices import SizeChoices


class Category(SoftDeleteModel, BaseModel):
    name= models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique = True)
    description = models.TextField(blank=True)

    images = models.ImageField(upload_to="images/categories/", blank=True, null=True)
    is_active = models.BooleanField(default=True)

    objects = CategoryManager()
    all_objects = models.Manager()


    class Meta:
        ordering=["name"]
        verbose_name_plural = "Categories"


    def __str__(self):
        return self.name
    

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Brand(BaseModel, SoftDeleteModel):
    name = models.CharField(max_length=120, unique=True)
    slug= models.SlugField(max_length=140, unique=True)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to="images/brands/", blank=True, null=True)

    active = models.BooleanField(default=True)

    objects = BrandManager()
    all_objects = models.Manager()

    class Meta:
        ordering=['name']

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)


class Product(BaseModel, SoftDeleteModel):
    category = models.ForeignKey(Category,on_delete=models.PROTECT, related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name="products")
    name = models.CharField(max_length=180)
    slug = models.SlugField(max_length=220)
    description = models.TextField()
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    main_image = models.ImageField(upload_to="images/products/main/", blank=True, null=True)

    objects = ProductManager()
    all_objects = models.Manager()

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["is_active", "is_available"]),
            models.Index(fields=["is_featured"]),
        ]
    
    def __str__(self):
        return self.name
    
    def clean(self):
        if self.discount_price and self.discount_price > self.base_price:
            raise ValidationError("Discount Price cann't be greater than the base price")

    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        self.full_clean()
        super().save(*args, **kwargs)

    @property 
    def current_price(self):
        return self.discount_price if self.discount_price is not None else self.base_price


    @property
    def has_discount(self):
        return self.discount_price is not None
    
    @property
    def total_stock(self):
        return self.variants.filter(is_active=True).aggregate(total=models.Sum("stock")).get("total") or 0



class ProductImage(BaseModel):
    product = models.ForeignKey(Product, on_delete= models.CASCADE, related_name="images")
    images = models.ImageField(upload_to="images/product/gallery")
    alt_text = models.CharField(max_length=255, blank=True)
    is_primary = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "id"]

    def __str__(self):
        return f"{self.product.name} images"


class ProductVariant(BaseModel):
    product = models.ForeignKey(Product, on_delete = models.CASCADE, related_name="variants")
    size = models.CharField(max_length=10, choices=SizeChoices.choices)
    color = models.CharField(max_length=50)
    sku = models.CharField(max_length=80, unique=True)
    stock = models.PositiveIntegerField(default = 0)
    price_override = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)


    class Meta:
        ordering = ["product", "size", "color"]
        unique_together = ("product", "size", "color")
        indexes = [
            models.Index(fields=["sku"]),
            models.Index(fields=["product", "is_active"])
        ]
    
    def __str__(self):
        return f"{self.product.name} - {self.size} - {self.color}"

    
    def clean(self):
        if self.price_override is not None and self.price_override < Decimal("0.00"):
            raise ValidationError("Price override cannot be negative.")

    @property
    def final_price(self):
        return self.price_overrride if self.price_overrride is not None else self.product.current_price
    

    @property
    def is_in_stock(self):
        return self.stock > 0 and self.is_active
    







"""
later
separate color models
separate size models
inventory history
SEO fields
review support 
discount/ coupon logic
"""