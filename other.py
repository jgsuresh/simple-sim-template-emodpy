import emod_api.demographics.Demographics as Demographics

import manifest


def build_demographics_from_file():
    file_path = manifest.demographics_file_path
    demo = Demographics.from_file(file_path)
    return demo

