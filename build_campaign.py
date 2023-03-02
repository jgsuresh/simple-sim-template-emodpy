# Put functions relating to interventions here

from emodpy_malaria.interventions.drug_campaign import add_drug_campaign
from emodpy_malaria.interventions.inputeir import add_InputEIR

import manifest
from jsuresh_helpers.running_emodpy import build_standard_campaign_object


def build_campaign():
    campaign = build_standard_campaign_object(manifest=manifest)

    add_InputEIR(campaign, monthly_eir=[5]*12)
    add_drug_campaign(campaign, campaign_type="MDA", drug_code="PPQ", start_days=[1], coverage=1.0)

    return campaign
