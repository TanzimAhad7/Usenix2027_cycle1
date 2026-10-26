"""Frozen wall-time limit, independent of whether scientific results are good."""
from .common import BudgetStop

class CampaignBudgetStop(BudgetStop):
    """Collection ends; preserved effects and incomplete schedule remain evidence."""

