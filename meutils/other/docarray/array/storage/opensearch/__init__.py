from abc import ABC

from meutils.docarray_.array.storage.opensearch.backend import BackendMixin, OpenSearchConfig
from meutils.docarray_.array.storage.opensearch.find import FindMixin
from meutils.docarray_.array.storage.opensearch.getsetdel import GetSetDelMixin
from meutils.docarray_.array.storage.opensearch.seqlike import SequenceLikeMixin

__all__ = ['StorageMixins', 'OpenSearchConfig']


class StorageMixins(FindMixin, BackendMixin, GetSetDelMixin, SequenceLikeMixin, ABC):
    ...
