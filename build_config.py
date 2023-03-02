from emodpy_malaria.malaria_config import set_team_defaults

import manifest
from jsuresh_helpers.running_emodpy import set_log_level


def set_full_config(config):
    set_core_config_params(config)
    set_project_config_params(config)
    return config


def set_core_config_params(config):
    config.parameters.Simulation_Type = "MALARIA_SIM"
    set_team_defaults(config, manifest)

    # IP white list (non-schema)
    config.parameters["Disable_IP_Whitelist"] = 1


def set_project_config_params(config):
    config.parameters.Enable_Initial_Prevalence = 0

    config.parameters.Enable_Vital_Dynamics = 0
    config.parameters.Enable_Natural_Mortality = 0
    config.parameters.Enable_Demographics_Birth = 0
    config.parameters.Age_Initialization_Distribution_Type = "DISTRIBUTION_SIMPLE"

    config.parameters.Climate_Model = "CLIMATE_CONSTANT"
    config.parameters.Base_Air_Temperature = 27
    config.parameters.Base_Land_Temperature = 27

    set_log_level(config)