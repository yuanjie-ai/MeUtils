from abc import ABC

from meutils.docarray_.array.storage.weaviate.backend import BackendMixin, WeaviateConfig
from meutils.docarray_.array.storage.weaviate.find import FindMixin
from meutils.docarray_.array.storage.weaviate.getsetdel import GetSetDelMixin
from meutils.docarray_.array.storage.weaviate.seqlike import SequenceLikeMixin

__all__ = ['StorageMixins', 'WeaviateConfig']


class StorageMixins(FindMixin, BackendMixin, GetSetDelMixin, SequenceLikeMixin, ABC):
    ...
