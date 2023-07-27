from meutils.docarray_.document.mixins.attribute import GetAttributesMixin
from meutils.docarray_.document.mixins.audio import AudioDataMixin
from meutils.docarray_.document.mixins.blob import BlobDataMixin
from meutils.docarray_.document.mixins.content import ContentPropertyMixin
from meutils.docarray_.document.mixins.convert import ConvertMixin
from meutils.docarray_.document.mixins.dump import UriFileMixin
from meutils.docarray_.document.mixins.featurehash import FeatureHashMixin
from meutils.docarray_.document.mixins.image import ImageDataMixin
from meutils.docarray_.document.mixins.mesh import MeshDataMixin
from meutils.docarray_.document.mixins.multimodal import MultiModalMixin
from meutils.docarray_.document.mixins.plot import PlotMixin
from meutils.docarray_.document.mixins.porting import PortingMixin
from meutils.docarray_.document.mixins.property import PropertyMixin
from meutils.docarray_.document.mixins.protobuf import ProtobufMixin
from meutils.docarray_.document.mixins.pydantic import PydanticMixin
from meutils.docarray_.document.mixins.strawberry import StrawberryMixin
from meutils.docarray_.document.mixins.sugar import SingletonSugarMixin
from meutils.docarray_.document.mixins.text import TextDataMixin
from meutils.docarray_.document.mixins.video import VideoDataMixin


class AllMixins(
    ProtobufMixin,
    PydanticMixin,
    StrawberryMixin,
    PropertyMixin,
    ContentPropertyMixin,
    ConvertMixin,
    AudioDataMixin,
    ImageDataMixin,
    TextDataMixin,
    MeshDataMixin,
    VideoDataMixin,
    BlobDataMixin,
    PlotMixin,
    UriFileMixin,
    SingletonSugarMixin,
    PortingMixin,
    FeatureHashMixin,
    GetAttributesMixin,
    MultiModalMixin,
):
    """All plugins that can be used in :class:`Document`."""

    ...
