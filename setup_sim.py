from emodpy_malaria.config import set_team_defaults, set_species, get_species_params
from jsuresh_helpers.running_dtk import set_executable, add_params_csv_to_dtk_config_builder
from jsuresh_helpers.uncategorized import load_csv_into_dictionary
from jsuresh_helpers.windows_filesystem import get_dropbox_location

import manifest

dropbox_folder = get_dropbox_location()
input_folder = dropbox_folder + "projects/jsuresh_sim_examples/example_input_folder/"
# bin_folder = input_folder + "bin"
params_csv_filename = input_folder + "params.csv"


def set_ento(config):
    set_species(config, ["arabiensis", "funestus"])

    # set_species_param #fixme Asking Jonathan to make this function for me


    '''

    set_species_param(cb, 'arabiensis', 'Indoor_Feeding_Fraction', 0.5)
    set_species_param(cb, 'arabiensis', 'Adult_Life_Expectancy', 20)
    set_species_param(cb, 'arabiensis', 'Anthropophily', 0.65)
    set_species_param(cb, 'arabiensis', 'Vector_Sugar_Feeding_Frequency', "VECTOR_SUGAR_FEEDING_NONE")

    set_species_param(cb, 'funestus', "Indoor_Feeding_Fraction", 0.9)
    set_species_param(cb, 'funestus', 'Adult_Life_Expectancy', 20)
    set_species_param(cb, 'funestus', 'Anthropophily', 0.65)
    set_species_param(cb, 'funestus', 'Vector_Sugar_Feeding_Frequency', "VECTOR_SUGAR_FEEDING_NONE")
    '''


def set_project_specific_params(config):
    config.parameters.Num_Cores = 2
    config.parameters.Climate_Model = "CLIMATE_BY_DATA"
    # config.parameters.Enable_Vector_Migration = 1

    set_ento(config)

# def set_larval_habitat() #fixme Unclear if necessary.  Jonathan had this
#     lhm = dfs.schema_to_config_subnode( manifest.schema_file, ["idmTypes","idmType:VectorHabitat"] )
#     lhm.parameters.Max_Larval_Capacity = 11250000000
#     lhm.parameters.Vector_Habitat_Type = "TEMPORARY_RAINFALL"
#     lhm.parameters.finalize()
#     conf.get_species_params( config, "gambiae" ).Larval_Habitat_Types.append( lhm.parameters )


def build_project_config(config):

    config.parameters.Simulation_Type = "MALARIA_SIM"
    # malaria sim defaults
    set_team_defaults(config, manifest)

    # project params
    set_project_specific_params(config)

    return config
