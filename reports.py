# Put functions relating to reports here

from emodpy_malaria.reporters.builtin import add_drug_status_report, add_report_intervention_pop_avg


def add_reports(emod_task, manifest):
    add_drug_status_report(emod_task, manifest)
    add_report_intervention_pop_avg(emod_task, manifest)