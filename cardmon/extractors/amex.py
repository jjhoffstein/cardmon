from .base import BaseSchumerExtractor

class AmexExtractor(BaseSchumerExtractor):
    @property
    def row_selector(self): return 'tr, [class*="rate"], [class*="fee"]'
