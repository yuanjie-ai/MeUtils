from abc import ABC

from meutils.docarray_.array.storage.sqlite.backend import BackendMixin, SqliteConfig
from meutils.docarray_.array.storage.sqlite.getsetdel import GetSetDelMixin
from meutils.docarray_.array.storage.sqlite.seqlike import SequenceLikeMixin
from meutils.docarray_.array.storage.memory.find import (
    FindMixin,
)  # temporary delegate to in-memory find API

__all__ = ['StorageMixins', 'SqliteConfig']


class StorageMixins(FindMixin, BackendMixin, GetSetDelMixin, SequenceLikeMixin, ABC):
    ...
