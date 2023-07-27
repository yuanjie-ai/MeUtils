from meutils.docarray_.score.data import NamedScoreData
from meutils.docarray_.score.mixins import AllMixins
from meutils.docarray_.base import BaseDCType


class NamedScore(AllMixins, BaseDCType):
    _data_class = NamedScoreData
    _post_init_fields = ()
