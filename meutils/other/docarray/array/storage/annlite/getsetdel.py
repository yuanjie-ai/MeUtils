from typing import Iterable, Dict

from meutils.docarray_.array.storage.annlite.helper import OffsetMapping
from meutils.docarray_.array.storage.base.getsetdel import BaseGetSetDelMixin
from meutils.docarray_.array.storage.base.helper import Offset2ID
from meutils.docarray_.array.memory import DocumentArrayInMemory
from meutils.docarray_ import Document, DocumentArray


class GetSetDelMixin(BaseGetSetDelMixin):
    """Implement required and derived functions that power `getitem`, `setitem`, `delitem`"""

    # essential methods start

    def _get_doc_by_id(self, _id: str) -> 'Document':
        doc = self._annlite.get_doc_by_id(_id)
        if doc is None:
            raise KeyError(f'Can not find Document with id=`{_id}`')
        return doc

    def _set_doc_by_id(self, _id: str, value: 'Document'):
        if _id != value.id:
            self._del_doc_by_id(_id)

        value.embedding = self._map_embedding(value.embedding)
        docs = DocumentArrayInMemory([value])

        self._annlite.update(docs)

    def _del_doc_by_id(self, _id: str):
        # delete the root document
        self._del_docs_by_ids([_id])

    def _clear_storage(self):
        self._annlite.clear()

    def _set_docs_by_ids(self, ids, docs: Iterable['Document'], mismatch_ids: Dict):
        for _id, doc in zip(ids, docs):
            doc.embedding = self._map_embedding(doc.embedding)
            self._set_doc_by_id(_id, doc)

    def _del_docs_by_ids(self, ids):
        self._annlite.delete(ids)

    def __del__(self) -> None:
        self._annlite.close()

    def _load_offset2ids(self):
        if self._list_like:
            self._offsetmapping = OffsetMapping(
                data_path=self._config.data_path, in_memory=False
            )
            self._offsetmapping.create_table()
            self._offset2ids = Offset2ID(
                self._offsetmapping.get_all_ids(),
                list_like=self._list_like,
            )
        else:
            self._offset2ids = Offset2ID(
                [],
                list_like=self._list_like,
            )

    def _save_offset2ids(self):
        if self._list_like:
            self._offsetmapping.drop()
            self._offsetmapping.create_table()
            self._offsetmapping._insert(
                [(i, doc_id) for i, doc_id in enumerate(self._offset2ids.ids)]
            )
