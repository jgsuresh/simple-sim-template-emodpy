from emodpy.bamboo import get_model_files
from emodpy.emod_task import EMODTask
from emodpy.utils import EradicationBambooBuilds
from idmtools.core.platform_factory import Platform

import manifest

platform = Platform("SLURM")

print("Creating EMODTask (from files)...")

task = EMODTask.from_default2(
    config_path="config.json",
    eradication_path=manifest.eradication_path,
    campaign_builder=build_camp,
    schema_path=manifest.schema_file,
    param_custom_cb=set_param_fn,
    ep4_custom_cb=None,
    demog_builder=build_demog,
    plugin_report=None # report
)


'''
def general_sim( erad_path, ep4_scripts ):
    """
    This function is designed to be a parameterized version of the sequence of things we do 
    every time we run an emod experiment. 
    """
    print_params()

    platform = Platform("SLURM")

    #pl = RequirementsToAssetCollection( platform, requirements_path=manifest.requirements )

    # create EMODTask 
    print("Creating EMODTask (from files)...")

    task = EMODTask.from_default2(
        config_path="my_config.json",
        eradication_path=manifest.eradication_path,
        campaign_builder=build_camp,
        schema_path=manifest.schema_file,
        param_custom_cb=set_param_fn,
        ep4_custom_cb=None,
        demog_builder=build_demog,
        plugin_report=None # report
    )

    print("Adding asset dir...")
    task.common_assets.add_directory(assets_directory=manifest.assets_input_dir)
    print("Adding local assets (py scripts mainly)...")

    if ep4_scripts is not None:
        for asset in ep4_scripts:
            pathed_asset = Asset(pathlib.PurePath.joinpath(manifest.ep4_path, asset), relative_path="python")
            task.common_assets.add_asset(pathed_asset)

    # Create simulation sweep with builder
    builder = SimulationBuilder()
    builder.add_sweep_definition( update_sim_random_seed, range(params.nSims) )

    # create experiment from builder
    print( f"Prompting for COMPS creds if necessary..." )
    experiment  = Experiment.from_builder(builder, task, name=params.exp_name)

    #other_assets = AssetCollection.from_id(pl.run())
    #experiment.assets.add_assets(other_assets)

    # The last step is to call run() on the ExperimentManager to run the simulations.
    experiment.run(wait_until_done=True, platform=platform)

    # Check result
    if not experiment.succeeded:
        print(f"Experiment {experiment.uid} failed.\n")
        exit()

    print(f"Experiment {experiment.uid} succeeded.")

    # Save experiment id to file
    with open("COMPS_ID", "w") as fd:
        fd.write(experiment.uid.hex)
    print()
    print(experiment.uid.hex)


def run_test( erad_path ):
    general_sim( erad_path, manifest.my_ep4_assets )
'''



if __name__ == "__main__":
    # TBD: user should be allowed to specify (override default) erad_path and input_path from command line
    plan = EradicationBambooBuilds.MALARIA_LINUX
    print("Retrieving Eradication and schema.json from Bamboo...")
    get_model_files(plan, params)
    print("...done.")
    run_test(params.eradication_path)
