from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

from .core import iqrm_mask
from .tests import test
