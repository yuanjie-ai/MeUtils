from abc import ABC

from meutils.docarray_.array.storage.memory.backend import BackendMixin
from meutils.docarray_.array.storage.memory.find import FindMixin
from meutils.docarray_.array.storage.memory.getsetdel import GetSetDelMixin
from meutils.docarray_.array.storage.memory.seqlike import SequenceLikeMixin

__all__ = ['StorageMixins']


class StorageMixins(FindMixin, BackendMixin, GetSetDelMixin, SequenceLikeMixin, ABC):
    ...
