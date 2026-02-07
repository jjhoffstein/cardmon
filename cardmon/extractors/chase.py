from .base import BaseSchumerExtractor

class ChaseExtractor(BaseSchumerExtractor):
    label_map = dict(
        purchase_apr=['purchase', 'apr', 'annual'],
        balance_transfer_apr=['balance transfer', 'apr'],
        cash_advance_apr=['cash advance', 'apr'],
        annual_fee=['annual', 'fee'],
        foreign_tx_fee=['foreign'],
        late_fee=['late', 'payment'],
    )

    @property
    def cell_tags(self): return ['td']
