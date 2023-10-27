import pathlib
from pkgutil import ModuleInfo, iter_modules

_cogs: list[ModuleInfo] = []
_cogs.extend(
    [
        module
        for module in iter_modules(__path__, prefix=__package__ + ".")
        if not module.name.rsplit(".")[-1].startswith("_")
    ]
)

COGS = _cogs
