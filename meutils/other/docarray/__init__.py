__version__ = '0.21.0'

import os

from meutils.docarray_.document import Document
from meutils.docarray_.array import DocumentArray
from meutils.docarray_.dataclasses import dataclass, field
from meutils.docarray_.helper import login, logout

if 'DA_RICH_HANDLER' in os.environ:
    from rich.traceback import install

    install()
