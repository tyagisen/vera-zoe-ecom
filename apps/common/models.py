from django.db import models
import uuid
from django.utils import timezone


class BaseModel(models.Model):
    """
    This is base model is created for other models not to repeat same code over again.(DRY principle)
    UUID:-id that never repeats even if whole world generates millions at the same time.(128 bit 32 hex and 4 dashes; 8-4-4-4-12)
    Project is scalable so need to do this even it has certain drabacks it make slow but good things about uuid wins against cons. 
    Better for microservices and distributed system; multiple servers, load balancing, microservices
    UUID ensures unique IDs everywhere without depending on central database.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable =False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        abstract=True





class SoftDeleteQuerySet(models.QuerySet):
    def delete(self):
        return super().update(is_deleted=True, deleted_at=timezone.now())
    
    def hard_delete(self):
        return super().delete()
    
    def alive(self):
        return self.filter(is_deleted=False)
    
    def dead(self):
        return self.filter(is_deleted=True)


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db).filter(is_deleted=False)
    

class AllObjectsManager(models.Manager):
    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db)
    
class DeleteObjectsManager(models.Manager):
    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db).filter(is_deleted=True)


class SoftDeleteModel(models.Model):
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)


    # Delete Managers
    objects=SoftDeleteManager() #It hides where is_deleted is False
    all_objects = AllObjectsManager() #It shows all objects including is_deleted=False
    deleted_objects=DeleteObjectsManager() # Return deleted objects or is_deleted=True


    class Meta:
        abstract=True


    def delete(self, using=None, keep_parents=False):
        '''
        This parameter are already builtin the django so it expects the parameter
        This is django builtin delete method it is just method overriding so we keep as it is in real method
        using=None actually using tells which db to use as this method will be used for multiple db.
        keep_parents=False is to tell not to create multiple database as for the table. deleting child row deletes parent row
        '''
        self.is_deleted=True
        self.deleted_at=timezone.now()
        '''
        This method save(update_fields=['is_deleted', 'detelted_at'] is done is order to protect
        from saving the whole more but we need just is_deleted, deleted_at to be updated also
        we dont want to trigger some signals it is safe and sound.
        '''
        self.save(update_fields=["is_deleted", "deleted_at"])


    def hard_delete(self, using=None, keep_parents=False):
        """
        Permanent delete class
        """
        return super().delete(using=using, keep_parents=keep_parents)
    

    def restore(self, using=None, keep_parents=False):
        """
        This method stores deleted items back
        """
        self.is_deleted=False
        self.deleted_at = None
        self.save(update_fields=["is_deleted", "deleted_at"])


class SlugModel(models.Model):
    slug = models.SlugField(unique=True)

    class Meta:
        abstract = True
