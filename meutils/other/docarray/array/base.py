from typing import MutableSequence, TYPE_CHECKING, Union, Iterable

from meutils.docarray_ import Document

if TYPE_CHECKING:  # pragma: no cover
    from meutils.docarray_.typing import T


class BaseDocumentArray(MutableSequence[Document]):
    def __init__(self, *args, storage: str = 'memory', **kwargs):
        super().__init__()
        self._init_storage(*args, **kwargs)
        self._init_subindices(*args, **kwargs)

    def __add__(self: 'T', other: Union['Document', Iterable['Document']]) -> 'T':
        v = type(self)(self)
        v.extend(other)
        return v
