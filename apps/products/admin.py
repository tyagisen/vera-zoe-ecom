from django.contrib import admin
from apps.products.models import Brand, Category, Product, ProductImage, ProductVariant


"""
The below TabularInline does is provides easy way to manage child objects quickly fields are simple and few.
So, ProductImage is child of product so, ProductImage is in tabularInline so that it could be
included in the product saying inlines = []. Now, what happens is we can see product image objects
in the product and also able to add there without selecting for particular product.
and extra = 1 is to give one extra empty row to add new product Image or product variant whatever
works accordingly.
"""
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1



"""
There is prepopulated_fields which automatically fills one field based on another field while typing
example when i type name with i love you it automaticall fill slug saying i-love-you. so, name is the source 
for slug to fill. As for backend we use save(self, *args, **kwargs)
"""
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug", "is_active", "created_at")
    list_filter = ("is_active", "is_deleted")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name", )}



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "category",
        "brand",
        "base_price",
        "discount_price",
        "is_active",
        "is_available",
        "is_featured",
        "created_at",
    )
    list_filter = (
        "is_active",
        "is_available",
        "is_featured",
        "category",
        "brand",
        "is_deleted",
    )
    search_fields = (
        "name",
        "slug",
        "description"
    )
    prepopulated_fields = {"slug":("name",)}
    inlines = [ProductImageInline, ProductVariantInline]


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "is_primary", "display_order", "created_at")
    list_filter = ("is_primary",)
    search_fields = ("product__name", "alt_text",)


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "size", "color", "sku", "stock", "price_override", "is_active")
    list_filter = ("size", "color", "is_active")
    search_fields = ("product__name", "sku", "color")