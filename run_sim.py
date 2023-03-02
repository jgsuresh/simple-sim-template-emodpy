import pathlib

from emodpy.bamboo import get_model_files
from emodpy.emod_task import EMODTask
from emodpy.utils import EradicationBambooBuilds
from idmtools.builders import SimulationBuilder
from idmtools.core.platform_factory import Platform

import manifest

from idmtools.entities.experiment import Experiment

from build_campaign import build_campaign
from build_config import set_full_config
from other import build_demographics_from_file
from reports import add_reports
from setup_sim import build_project_config
from sweeps import update_sim_bic, update_sim_random_seed


def create_and_submit_experiment():
    experiment_name = "test_sim"

    platform = Platform("Calculon", num_cores=1, node_group="idm_48cores", priority="Highest")

    # =========================================================

    task = EMODTask.from_default2(
        config_path="config.json",
        eradication_path=manifest.eradication_path,
        campaign_builder=build_campaign,
        # campaign_builder=None,
        schema_path=manifest.schema_file,
        param_custom_cb=set_full_config,
        ep4_custom_cb=None,
        demog_builder=build_demographics_from_file
    )

    add_reports(task, manifest)

    # Create simulation sweep with builder
    builder = SimulationBuilder()
    builder.add_sweep_definition(update_sim_random_seed, [0])

    # Create experiment
    print( f"Prompting for COMPS creds if necessary..." )
    experiment = Experiment.from_builder(builder, task, name=experiment_name)
    experiment.run(wait_until_done=True, platform=platform)

    # Check result
    if not experiment.succeeded:
        print(f"Experiment {experiment.uid} failed.\n")
        exit()

    print(f"Experiment {experiment.uid} succeeded.")



if __name__ == "__main__":
    plan = EradicationBambooBuilds.MALARIA_LINUX

    # Download latest Eradication
    print("Retrieving Eradication and schema.json packaged with emod-malaria...")
    import emod_malaria.bootstrap as emod_malaria_bootstrap
    emod_malaria_bootstrap.setup(pathlib.Path(manifest.eradication_path).parent)
    print("...done.")

    create_and_submit_experiment()
