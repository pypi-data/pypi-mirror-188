from django.core.paginator import Page, Paginator
from django.utils.functional import cached_property


class EstimatedObjectsPagination(Paginator):
    def __init__(self, *args, **kwargs):
        self.object_count = kwargs.pop("object_count", None)
        super().__init__(*args, **kwargs)

    @cached_property
    def count(self):
        if self.object_count is not None:
            return self.object_count
        return super().count

    def _get_page(self, *args, **kwargs):
        return EstimatedObjectsPage(*args, **kwargs)


class EstimatedObjectsPage(Page):
    """
    Handle page pagination for estimated object count.
    """

    def has_next(self) -> bool:
        if not self.object_list:
            return False
        return super().has_next()
