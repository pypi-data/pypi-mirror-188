import uuid
from io import BytesIO

import phonenumbers
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.enums import TextChoices
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from PIL import Image, ImageDraw

from medux.common.constants import UserColors, random_user_color
from medux.common.tools import resize_image


class AutoDateTimeField(models.DateTimeField):
    def pre_save(self, model_instance, add):
        return timezone.now()


class SingletonModel(models.Model):
    """A base model that only can haz one instance."""

    class Meta:
        abstract = True

    @classmethod
    def get_instance(cls):
        """:return: the current instance if available, else an empty instance."""
        if cls.objects.exists():
            return cls.objects.first()
        else:
            return cls()

    def save(self, *args, **kwargs):
        if not self.pk and Vendor.objects.exists():
            raise ValidationError(
                f"There can be only one {self.__class__.__name__} instance."
            )
        super().save(*args, **kwargs)


class CreatedModifiedModel(models.Model):
    """A simple mixin for model classes that need to have created/modified fields."""

    created = models.DateTimeField(editable=False, default=timezone.now)
    modified = AutoDateTimeField(default=timezone.now)

    class Meta:
        abstract = True


# taken from https://adriennedomingus.medium.com/soft-deletion-in-django-e4882581c340
class SoftDeletionQuerySet(models.QuerySet):
    def delete(self):
        return super().update(deleted_at=timezone.now())

    def hard_delete(self):
        return super().delete()

    def alive(self):
        return self.filter(deleted_at=None)

    def dead(self):
        return self.exclude(deleted_at=None)


class SoftDeletionManager(models.Manager):
    """Custom Django Manager for soft-delete queries.

    This object manager transparently only fetches objects from the
    database that are not soft-deleted."""

    # TODO: use https://github.com/scoursen/django-softdelete instead
    # https://medium.com/@adriennedomingus/soft-deletion-in-django-e4882581c340
    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop("alive_only", True)
        super().__init__(*args, **kwargs)

    def get_queryset(self):
        if self.alive_only:
            return SoftDeletionQuerySet(self.model).filter(deleted_at=None)
        return SoftDeletionQuerySet(self.model)

    def hard_delete(self):
        return self.get_queryset().hard_delete()


class BaseModel(CreatedModifiedModel):
    """An abstract base class with common used functionality.

    Every relevant model that needs soft_deletion in MedUX should inherit BaseModel.

    It provides:
    * basic created/modified timestamps for auditing
    * a soft delete functionality: Deleted items are just marked as deleted.
    """

    class Meta:
        abstract = True

    deleted_at = models.DateTimeField(
        editable=False, blank=True, null=True, default=None
    )

    row_version = models.PositiveIntegerField(editable=False, default=0)

    # The standard manager only returns not-soft-deleted objects
    objects = SoftDeletionManager()

    # The all_objects Manager returns ALL objects, even soft-deleted ones
    all_objects = SoftDeletionManager(alive_only=False)

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = timezone.now()
        self.save()

    def hard_delete(self):
        super().delete()


class SexChoices(TextChoices):
    # FIXME: replace with AdministrativeGender
    MALE = "male", _("male")
    FEMALE = "female", _("female")


class Tenant(models.Model):
    """A MedUX tenant, like an MD who "owns" a homepage, or a practice
    owner with a MedUX appliance."""

    class Meta:
        verbose_name = _("Tenant")
        verbose_name_plural = _("Tenants")

    uuid = models.UUIDField(default=uuid.uuid4, unique=True)

    title = models.CharField(_("Title"), max_length=50, blank=True)
    first_name = models.CharField(_("First name"), max_length=255)
    last_name = models.CharField(_("Last name"), max_length=255)
    sex = models.CharField(_("Sex"), max_length=25, choices=SexChoices.choices)
    address = models.CharField(_("Address"), max_length=255)
    phone = models.CharField(_("Phone"), max_length=30, blank=True)
    email = models.EmailField(
        _("Email"), unique=True, default=None, blank=True, null=True
    )
    #: The picture/logo of the tenant. If None, the initials are used to create a picture
    picture = models.ImageField(_("Picture"), blank=True, null=True)

    def get_picture_from_initials(self):
        # TODO: make colors configurable
        canvas = Image.new("RGB", (128, 128), "grey")

        draw = ImageDraw.Draw(canvas)
        # font = ImageFont.truetype("FreeMono.ttf", 48)
        draw.text(
            (4, 4),
            self.initials(),
            # font=font,
            fill=(200, 50, 50),
        )
        blob = BytesIO()
        canvas.save(blob, "JPEG")  # TODO: png
        del blob
        return canvas

    @property
    def name(self):
        # TODO: if user exists, take his name.
        title = f"{self.title} " if self.title else ""
        return f"{title}{self.last_name}, {self.first_name}"

    def __str__(self):
        return f"{self.name}"

    def natural_key(self):
        return self.first_name, self.last_name

    def get_absolute_url(self):
        return reverse("tenant:detail", kwargs={"pk": self.pk})

    def initials(self):
        return f"{self.last_name[0].upper()}{self.first_name[0].upper()}"


class CommonUser(AbstractUser):
    """The base user for MedUX, MedUX Online, MedUX Update Server etc.

    A user usually belongs to a tenant, except for e.g. admin users.
    """

    title = models.CharField(max_length=25, blank=True, null=True)
    # FIXME: Admin user should belong to Admin tenant - no null necessary here
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, null=True)

    color = models.CharField(
        verbose_name=_("User color"),
        max_length=25,
        choices=UserColors.choices,
        default=random_user_color,
    )

    def __str__(self) -> str:
        title = f"{self.title} " if self.title else ""
        if self.first_name and self.last_name:
            return f"{title}{self.first_name} {self.last_name}"
        else:
            return self.username

    def natural_key(self) -> str:
        return self.username

    def get_absolute_url(self) -> str:
        """Get url for user's detail view.
        :returns str: URL for user detail."""
        return reverse("user:detail", kwargs={"pk": self.pk})

    avatar = models.ImageField(upload_to="user_avatars/", null=True, blank=True)

    @property
    def job_title(self):
        return "Job title"  # TODO: add job title

    def save(self, commit=True, *args, **kwargs):
        """Resizes avatar image before saving."""
        if commit:
            if self.avatar:
                resize_image(self.avatar, 250, 250)
            super().save(*args, **kwargs)

    @property
    def channels_group_name(self):
        """Returns a group name based on the user's id to be used by Django Channels.
        Example usage:
        """
        return f"user_{self.id}"


class TenantModelMixin(models.Model):
    """A mixin that can be added to a model to mark it as belonging to a tenant.

    It adds a ``tenant`` ForeignKey to the model."""

    class Meta:
        abstract = True

    tenant = models.ForeignKey(
        Tenant,
        verbose_name=_("Tenant"),
        on_delete=models.CASCADE,
    )


# class OptionalTenantModelMixin(models.Model):
#     """A mixin that can be added to a model to mark it as
#     optionally belonging to a tenant.
#
#     It adds a (nullable) ``tenant`` ForeignKey to the model."""
#
#     class Meta:
#         abstract = True
#
#     tenant = models.ForeignKey(
#         Tenant,
#         verbose_name=_("Tenant"),
#         on_delete=models.CASCADE,
#         blank=True,
#         null=True,
#     )


# class TenantGroup(TenantModelMixin):
#     """A group within a tenant that has certain rights."""


def validate_phonenumber(number: str) -> bool:
    """return True iv given number is a possible phone number"""
    z = phonenumbers.parse(number)
    return phonenumbers.is_possible_number(z)


class Vendor(SingletonModel):
    """The vendor that is responsible for this MedUX appliance."""

    # TODO find an easy way to deploy data in Vendor model
    # maybe in a preferences.toml file?

    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    zip = models.CharField(max_length=10)
    city = models.CharField(max_length=50)
    phone = models.CharField(max_length=80, validators=[validate_phonenumber])
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.name
