from abc import ABC

from meutils.docarray_.array.storage.annlite.backend import BackendMixin, AnnliteConfig
from meutils.docarray_.array.storage.annlite.find import FindMixin
from meutils.docarray_.array.storage.annlite.getsetdel import GetSetDelMixin
from meutils.docarray_.array.storage.annlite.seqlike import SequenceLikeMixin

__all__ = ['StorageMixins', 'AnnliteConfig']


class StorageMixins(FindMixin, BackendMixin, GetSetDelMixin, SequenceLikeMixin, ABC):
    ...
