from .base import BaseManager


class EatraParamManager(BaseManager):
    def create_by_meta(self, meta):
        return self.create(
            name=meta.name,
            memo=meta.memo,
            value_tp=meta.value_tp,
        )
