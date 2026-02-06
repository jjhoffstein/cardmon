from pydantic import BaseModel

class Schumer(BaseModel):
    "Schumer box data from Terms & Conditions"
    purchase_apr: str|None = None
    balance_transfer_apr: str|None = None
    cash_advance_apr: str|None = None
    annual_fee: str|None = None
    foreign_tx_fee: str|None = None
    late_fee: str|None = None
    balance_transfer_fee: str|None = None

class SpendMultiplier(BaseModel):
    category: str
    points_per_dollar: float
    exclusions: str|None = None

class Credit(BaseModel):
    name: str
    amount: str
    frequency: str|None = None
    expiration: str|None = None

class TravelBenefit(BaseModel):
    name: str
    details: str
    restrictions: str|None = None

class Benefits(BaseModel):
    "Extracted benefits from card marketing page"
    bonus_points: int|None = None
    bonus_spend_required: int|None = None
    bonus_time_limit: str|None = None
    annual_fee: str|None = None
    first_year_waived: bool|None = None
    spend_multipliers: list[SpendMultiplier] = []
    travel_benefits: list[TravelBenefit] = []
    credits: list[Credit] = []
    elite_program: str|None = None
    elite_tier: str|None = None
    anniversary_bonus: str|None = None
    other_benefits: list[str] = []

class Card(BaseModel):
    "Card configuration"
    name: str
    url: str
    issuer: str
    selector: str|None = None
    tcs_url: str|None = None

class CheckResult(BaseModel):
    "Result of checking a card"
    name: str
    changed: bool
    error: str|None = None
    schumer: Schumer|None = None
    benefits: Benefits|None = None
    diff: str|None = None
