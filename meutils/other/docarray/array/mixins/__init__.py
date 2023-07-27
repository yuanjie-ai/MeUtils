from abc import ABC

from meutils.docarray_.array.mixins.content import ContentPropertyMixin
from meutils.docarray_.array.mixins.delitem import DelItemMixin
from meutils.docarray_.array.mixins.embed import EmbedMixin
from meutils.docarray_.array.mixins.empty import EmptyMixin
from meutils.docarray_.array.mixins.evaluation import EvaluationMixin
from meutils.docarray_.array.mixins.find import FindMixin
from meutils.docarray_.array.mixins.getattr import GetAttributeMixin
from meutils.docarray_.array.mixins.getitem import GetItemMixin
from meutils.docarray_.array.mixins.group import GroupMixin
from meutils.docarray_.array.mixins.io.binary import BinaryIOMixin
from meutils.docarray_.array.mixins.io.common import CommonIOMixin
from meutils.docarray_.array.mixins.io.csv import CsvIOMixin
from meutils.docarray_.array.mixins.io.dataframe import DataframeIOMixin
from meutils.docarray_.array.mixins.io.from_gen import FromGeneratorMixin
from meutils.docarray_.array.mixins.io.json import JsonIOMixin
from meutils.docarray_.array.mixins.io.pushpull import PushPullMixin
from meutils.docarray_.array.mixins.match import MatchMixin
from meutils.docarray_.array.mixins.parallel import ParallelMixin
from meutils.docarray_.array.mixins.plot import PlotMixin
from meutils.docarray_.array.mixins.post import PostMixin
from meutils.docarray_.array.mixins.pydantic import PydanticMixin
from meutils.docarray_.array.mixins.reduce import ReduceMixin
from meutils.docarray_.array.mixins.sample import SampleMixin
from meutils.docarray_.array.mixins.setitem import SetItemMixin
from meutils.docarray_.array.mixins.strawberry import StrawberryMixin
from meutils.docarray_.array.mixins.text import TextToolsMixin
from meutils.docarray_.array.mixins.traverse import TraverseMixin
from meutils.docarray_.array.mixins.dataloader import DataLoaderMixin


class AllMixins(
    GetAttributeMixin,
    GetItemMixin,
    SetItemMixin,
    DelItemMixin,
    ContentPropertyMixin,
    PydanticMixin,
    StrawberryMixin,
    GroupMixin,
    EmptyMixin,
    CsvIOMixin,
    JsonIOMixin,
    BinaryIOMixin,
    CommonIOMixin,
    EmbedMixin,
    PushPullMixin,
    FromGeneratorMixin,
    FindMixin,
    MatchMixin,
    TraverseMixin,
    PlotMixin,
    SampleMixin,
    PostMixin,
    TextToolsMixin,
    EvaluationMixin,
    ReduceMixin,
    ParallelMixin,
    DataframeIOMixin,
    DataLoaderMixin,
    ABC,
):
    """All plugins that can be used in :class:`DocumentArray`."""

    ...
