from jsuresh_helpers.comps import submit_experiment_to_comps
from setup_sim import build_project_cb

###################
# Run description #
###################
# Test run

##################################
# Core malaria config parameters #
##################################
cb = build_project_cb()


##################################
# Run-specific config parameters #
##################################
# e.g. simulation duration, serialization, input files
cb.set_param("Simulation_Duration", 4*365)


#################################################
# Campaign events that apply to ALL simulations #
#################################################
# add_standard_interventions(cb)

#####################
# Experiment sweeps #
#####################
modlists = []

# num_seeds = 1
# modlist = modfn_sweep_over_seeds(num_seeds)
# modlists.append(modlist)


####################
# Reports and logs #
####################
# add_standard_reports(cb)


###############################
# Submission/COMPs parameters #
###############################

comps_experiment_name = "example_experiment"
comps_priority = "Normal"
comps_coreset = "emod_abcd"


##################
# Job submission #
##################

if __name__=="__main__":
    submit_experiment_to_comps(cb, comps_experiment_name, comps_priority, comps_coreset, modlists=modlists)


