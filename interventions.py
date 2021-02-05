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


def build_campaign_with_standard_events():
    # Campaign object is built simply by importing
    campaign.schema_path = manifest.schema_file

    add_standard_interventions(campaign)




# Jonathan's function, for comparison:
# def build_camp():
#     """
#     Build a campaign input file for the DTK using emod_api.
#     Right now this function creates the file and returns the filename. If calling code just needs an asset that's fine.
#     """
#     import emod_api.campaign as camp
#     import emod_api.interventions.outbreak as ob
#     import emodpy_malaria.interventions.bednet as bednet
#
#     # This isn't desirable. Need to think about right way to provide schema (once)
#     camp.schema_path = manifest.schema_file
#
#     # print( f"Telling emod-api to use {manifest.schema_file} as schema." )
#     camp.add( bednet.Bednet( camp, start_day=100, coverage=1.0, killing_eff=1.0, blocking_eff=1.0, usage_eff=1.0, node_ids=[321] ) )
#     return camp