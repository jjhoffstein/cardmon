from .base import BaseSchumerExtractor
from .barclays import BarclaysExtractor
from .chase import ChaseExtractor
from .amex import AmexExtractor
from .citi import CitiExtractor
from .capital_one import CapitalOneExtractor

_EXTRACTORS = dict(barclays=BarclaysExtractor, chase=ChaseExtractor, amex=AmexExtractor, citi=CitiExtractor, capital_one=CapitalOneExtractor)

def get_extractor(issuer: str) -> BaseSchumerExtractor:
    cls = _EXTRACTORS.get(issuer, BarclaysExtractor)
    return cls()

__all__ = ['BaseSchumerExtractor', 'get_extractor']
