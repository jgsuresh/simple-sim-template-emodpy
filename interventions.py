# Put functions relating to interventions here


import emod_api.campaign as campaign
import emod_api.interventions.outbreak as outbreak
from emodpy_malaria.interventions.bednet import Bednet

import manifest

def add_standard_interventions(campaign):
    bednet_distribution = Bednet(campaign,
                                 start_day=100,
                                 coverage=1.0,
                                 killing_eff=1.0,
                                 blocking_eff=1.0,
                                 usage_eff=1.0,
                                 node_ids=[321])
    campaign.add(bednet_distribution)

def add_nonintervention_campaign_events(campaign):
    pass

def build_campaign_with_standard_events():
    # Campaign object is built simply by importing
    campaign.schema_path = manifest.schema_file

    add_standard_interventions(campaign)

    return campaign
