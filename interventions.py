# Put functions relating to interventions here

import pandas as pd
import numpy as np

import emod_api.campaign as campaign
import emod_api.interventions.outbreak as outbreak
from emodpy_malaria.interventions.bednet import Bednet

import manifest
from emodpy_malaria.interventions.diag_survey import add_diagnostic_survey
from emodpy_malaria.interventions.drug_campaign import add_drug_campaign, drug_configs_from_code, \
    BroadcastEventToOtherNodes
from emodpy_malaria.interventions.irs import IRSHousingModification
from emodpy_malaria.interventions.udbednet import UDBednet


def add_bednets(campaign):
    # simple bednet from example
    # bednet_distribution = Bednet(campaign,
    #                              start_day=100,
    #                              coverage=1.0,
    #                              killing_eff=1.0,
    #                              blocking_eff=1.0,
    #                              usage_eff=1.0,
    #                              node_ids=[1])
    # campaign.add(bednet_distribution)

    kariba_itn_age_dependence = {'youth_cov': 0.65,
                                 'youth_min_age': 5,
                                 'youth_max_age': 20}

    kariba_itn_seasonal_dependence = {'min_cov': 0.5,
                                      'max_day': 60}

    kariba_itn_discard_rates = {
        "Expiration_Period_Distribution": "DUAL_EXPONENTIAL_DISTRIBUTION",
        "Expiration_Period_Mean_1": 260,
        "Expiration_Period_Mean_2": 2106,
        "Expiration_Period_Proportion_1": 0.6
    }


    # Typical blocking and killing efficacy/waning are now code defaults!
    fancier_bednet_distribution = UDBednet(campaign,
                                           start_day=100,
                                           coverage=0.6,
                                           age_dependence=kariba_itn_age_dependence,
                                           seasonal_dependence=kariba_itn_seasonal_dependence,
                                           discard_config=kariba_itn_discard_rates,
                                           node_ids=[1])

    fancier_bednet_distribution_with_birth_trigger = UDBednet(campaign,
                                                              start_day=100,
                                                              coverage=0.6,
                                                              age_dependence=kariba_itn_age_dependence,
                                                              seasonal_dependence=kariba_itn_seasonal_dependence,
                                                              discard_config=kariba_itn_discard_rates,
                                                              triggers=["Births"],
                                                              node_ids=[1])
    #fixme This was generating a bug.  Test looking into this.


    campaign.add(fancier_bednet_distribution)
    campaign.add(fancier_bednet_distribution_with_birth_trigger)

def add_irs(campaign):
    irs_spray_event = IRSHousingModification(campaign,
                                             start_day=200,
                                             coverage=0.8,
                                             node_ids=[2]
                                             )
    campaign.add(irs_spray_event)

def add_drug_interventions(campaign):
    mda_event = add_drug_campaign(campaign,
                                  campaign_type='MDA',
                                  drug_code='DP',
                                  start_days=[50],
                                  coverage=0.5)

    msat_event = add_drug_campaign(campaign,
                                   campaign_type='MSAT',
                                   drug_code='AL',
                                   diagnostic_type='BLOOD_SMEAR_PARASITES',
                                   diagnostic_threshold=0,
                                   start_days=[75],
                                   coverage=0.8)

    # healthseeking_event = add_healthseeking()
    #fixme couldn't find this function

    campaign.add(mda_event)
    campaign.add(msat_event)
    # campaign.add(healthseeking_event)

def add_simple_rcd(campaign):
    simple_rcd_event = add_drug_campaign(campaign,
                                         campaign_type='rfMSAT',
                                         drug_code='AL',
                                         diagnostic_type='BLOOD_SMEAR_PARASITES',
                                         diagnostic_threshold=0,
                                         start_days=[2],
                                         coverage=0.7,
                                         trigger_coverage=0.01,
                                         listening_duration=1000)

    campaign.add(simple_rcd_event)

def add_simple_hs(campaign,
                  u5_hs_rate,
                  nodeIDs=None):
    o5_hs_rate = u5_hs_rate * 0.5

    def create_target_list(u5_hs_rate, o5_hs_rate):
        return [{'trigger': 'NewClinicalCase',
                 'coverage': u5_hs_rate,
                 'agemin': 0,
                 'agemax': 5,
                 'seek': 1,
                 'rate': 0.3},
                {'trigger': 'NewClinicalCase',
                 'coverage': o5_hs_rate,
                 'agemin': 5,
                 'agemax': 100,
                 'seek': 1,
                 'rate': 0.3},
                {'trigger': 'NewSevereCase',
                 'coverage': 0.9,
                 'agemin': 0,
                 'agemax': 5,
                 'seek': 1,
                 'rate': 0.5},
                {'trigger': 'NewSevereCase',
                 'coverage': 0.8,
                 'agemin': 5,
                 'agemax': 100,
                 'seek': 1,
                 'rate': 0.5}]

    hs_event = add_health_seeking(campaign,
                                  nodeIDs=nodeIDs,
                                  start_day=1,
                                  targets=create_target_list(u5_hs_rate, o5_hs_rate),
                                  drug=['Artemether', 'Lumefantrine'])

    campaign.add_event(hs_event)


def change_working_men_ips(campaign):
    # Initialize everyone as being at home:
    change_individual_property(campaign,
                               target_property_name="TravelerStatus",
                               target_property_value="NotTraveler",
                               start_day=0)

    # Initial setup:
    young = {'agemin': 10, 'agemax': 15}
    medium = {'agemin': 15.01, 'agemax': 65}
    old = {'agemin': 65.01, 'agemax': 70}

    change_individual_property(campaign,
                               target_property_name="TravelerStatus",
                               target_property_value="IsTraveler",
                               target_group=young,
                               start_day=1,
                               daily_prob=0.15,
                               max_duration=1
                               )

    change_individual_property(campaign,
                               target_property_name="TravelerStatus",
                               target_property_value="IsTraveler",
                               target_group=medium,
                               start_day=1,
                               daily_prob=0.3,
                               max_duration=1
                               )

    change_individual_property(campaign,
                               target_property_name="TravelerStatus",
                               target_property_value="IsTraveler",
                               target_group=old,
                               start_day=1,
                               daily_prob=0.2,
                               max_duration=1
                               )

def chw_rcd_manager(campaign, days_between_followups=7, max_distance_to_other_nodes_km=0):
    # CHW manager.  Triggered by Received_Treatment events with probability trigger_coverage, and allocates interventions if they are in stock.
    # The intervention in this case is to broadcast "Diagnostic_Survey_0" to the parent node, requesting an MSAT.
    # Note that this setup **should** be able to see all of the nodes, and have a single stock.

    request_msat_config = BroadcastEventToOtherNodes(
        Event_Trigger="Diagnostic_Survey_0",
        Include_My_Node=True,
        Node_Selection_Type=BroadcastEventToOtherNodes_Node_Selection_Type_Enum.DISTANCE_ONLY,
        Max_Distance_To_Other_Nodes_Km=max_distance_to_other_nodes_km)

    chw = CommunityHealthWorkerEventCoordinator(
        Initial_Amount_Constant=1,
        Initial_Amount_Distribution="CONSTANT_DISTRIBUTION",
        Amount_In_Shipment=1,
        Days_Between_Shipments=days_between_followups,
        Max_Stock=1,
        Max_Distributed_Per_Day=1,
        Intervention_Config=request_msat_config,
        Trigger_Condition_List=["Received_Treatment"],
        Waiting_Period=0)

    chw_event = CampaignEvent(Start_Day=1,
                              Nodeset_Config={"class": "NodeSetAll"},
                              Event_Coordinator_Config=chw)

    campaign.add_event(chw_event)


def rcd_followthrough(campaign, followup_sweep_coverage=1., delivery_method="MTAT", rdt_thresh=40,
                      ip_restrictions=None, target="Everyone", nodeIDs=None):
    # Listen for Diagnostic_Survey_0 and implement a diagnostic survey, then broadcast TestedPositive or TestedNegative.
    # Then, if TestedPositive, then administer drugs and broadcast Received_RCD_Drugs

    # Drug setup
    # drug_code = 'AL'
    # drug_configs = drug_configs_from_code(campaign, drug_code=drug_code)

    if delivery_method == "MTAT":
        mtat_response(campaign, followup_sweep_coverage, rdt_thresh=rdt_thresh, ip_restrictions=ip_restrictions, target=target, nodeIDs=nodeIDs)

    elif delivery_method == "MDA":
        mda_response(campaign, followup_sweep_coverage, ip_restrictions=ip_restrictions, target=target, nodeIDs=nodeIDs)

def mtat_response(campaign, followup_sweep_coverage, rdt_thresh=40, ip_restrictions=None, target="Everyone", nodeIDs=None):
    # Drug setup
    drug_code = 'AL'
    drug_configs = drug_configs_from_code(campaign, drug_code=drug_code)

    # set up events to broadcast when receiving reactive campaign drug
    receiving_drugs_event = {
        "class": "BroadcastEvent",
        "Broadcast_Event": "Received_RCD_Drugs"
    }

    event_config = drug_configs + [receiving_drugs_event]

    response_event = add_diagnostic_survey(campaign,
                                           coverage=followup_sweep_coverage,
                                           start_day=1,
                                           diagnostic_threshold=0,
                                           diagnostic_type='BLOOD_SMEAR_PARASITES',
                                           measurement_sensitivity=1. / rdt_thresh,
                                           trigger_condition_list=['Diagnostic_Survey_0'],
                                           event_name='Reactive MSAT level 0',
                                           positive_diagnosis_configs=event_config,
                                           listening_duration=-1,
                                           IP_restrictions=ip_restrictions,
                                           target=target,
                                           nodeIDs=nodeIDs)
    campaign.add_event(response_event)

def mda_response(campaign, followup_sweep_coverage, ip_restrictions=None, target="Everyone", nodeIDs=None):
    response_event = add_drug_campaign(campaign,
                                       coverage=followup_sweep_coverage,
                                       drug_code='AL',
                                       start_days=[1],
                                       campaign_type="MDA",
                                       trigger_condition_list=["Diagnostic_Survey_0"],
                                       listening_duration=-1,
                                       ind_property_restrictions=ip_restrictions,
                                       target_group=target,
                                       nodeIDs=nodeIDs
                                       )
    campaign.add_event(response_event)

def add_complex_rcd(campaign):
    chw_rcd_manager(campaign)
    rcd_followthrough(campaign)

def recurring_outbreak_as_importation(cb, outbreak_fraction=0.01, repetitions=-1, tsteps_btwn=365, target='Everyone', start_day=0, strain=(0,0), nodes={"class": "NodeSetAll"}, property_restrictions=[]):
    """
    Add introduction of new infections to the campaign using the
    **OutbreakIndividual** class. Outbreaks can be recurring.

    Args:
        cb: The The :py:class:`DTKConfigBuilder
            <dtk.utils.core.DTKConfigBuilder>` containing the campaign
            configuration.
        outbreak_fraction: The fraction of people infected by the outbreak (
            **Demographic_Coverage** parameter).
        repetitions: The number of times to repeat the intervention.
        tsteps_btwn_:  The number of time steps between repetitions.
        target: The individuals to target with the intervention. To
            restrict by age, provide a dictionary of {'agemin' : x, 'agemax' :
            y}. Default is targeting everyone.
        start_day: The day on which to start distributing the intervention
            (**Start_Day** parameter).
        strain: A two-element tuple defining (Antigen, Genome).
        nodes: A dictionary defining the nodes to apply this intervention to
            (**Nodeset_Config** parameter).
        outbreak_source: The source of the outbreak.

    Returns:
        A dictionary holding the fraction and the time steps between events.

        Example:
        ::

            cb = DTKConfigBuilder.from_defaults(sim_example)
            recurring_outbreak(cb, outbreak_fraction=0.005, repetitions=3,
                               tsteps_btwn=30, target={"agemin": 1, "agemax": 5},
                               start_day=0, strain=("A", "H2N2"),
                               nodes={"class": "NodeSetAll"},
                               outbreak_source="PrevalenceIncrease")

    """

    intervention_list = [OutbreakIndividual(Antigen=strain[0], Genome=strain[1]),
                         BroadcastEvent(Broadcast_Event="InfectionDropped")
                         ]

    outbreak_event = CampaignEvent(
        Start_Day=start_day,
        Event_Coordinator_Config=StandardInterventionDistributionEventCoordinator(
            Number_Repetitions=repetitions,
            Timesteps_Between_Repetitions=tsteps_btwn,
            Property_Restrictions=property_restrictions,
            Target_Demographic=StandardInterventionDistributionEventCoordinator_Target_Demographic_Enum[target],
            Demographic_Coverage=outbreak_fraction,
            Intervention_Config=MultiInterventionDistributor(Intervention_List=intervention_list)
        ),
        Nodeset_Config=nodes
    )

    cb.add_event(outbreak_event)
    return {'outbreak_fraction': outbreak_fraction,
            'tsteps_btwn': tsteps_btwn}



def add_standard_interventions(campaign):
    add_bednets(campaign)
    add_irs(campaign)
    add_drug_interventions(campaign)
    add_simple_rcd(campaign)

    # Test these once they have been translated over to emodpy
    # add_simple_hs(campaign)
    # change_working_men_ips(campaign)
    # add_complex_rcd(campaign)
    # recurring_outbreak_as_importation(campaign)




# def add_nonintervention_campaign_events(campaign):
#     change_working_men_ips(campaign)


def build_campaign_with_standard_events():
    # Campaign object is built simply by importing
    campaign.schema_path = manifest.schema_file

    add_standard_interventions(campaign)
    # add_nonintervention_campaign_events(campaign)

    return campaign
