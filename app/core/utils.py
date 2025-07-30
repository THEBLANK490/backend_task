from rest_framework import exceptions
from django.core.exceptions import ObjectDoesNotExist


def get_or_not_found(qs: object, **kwargs):
    """
    Utility function to get an object from queryset or raise NotFound exception if not found.

    Args:
        qs (object): The queryset to search for the object.
        **kwargs: Keyword arguments for filtering the queryset.

    Returns:
        object: The object retrieved from the queryset.

    Raises:
        exceptions.NotFound: If the object is not found in the queryset.
    """
    try:
        return qs.get(**kwargs)
    except ObjectDoesNotExist:
        raise exceptions.NotFound(f"{qs.model.__name__} instance not found")
