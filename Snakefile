rule save_coordinates:
    input:
        "src/scripts/fermipy_data.yml",
    output:
        "src/tex/output/download_coordinates.txt",
    conda:
        "environment.yml"
    script:
        "src/scripts/text_download_coordinates.py"


rule query_fermi_data:
    log:
        "src/data/workflow.log",
    input:
        "src/scripts/fermipy_data.yml",
    output:
        "src/data/Fermi_LAT/url_filenames.txt",
    conda:
        "environment_fermipy.yml"
    script:
        "src/scripts/query_fermi_data.py"


rule download_fermi_data_files:
    log:
        "src/data/workflow.log",
    input:
        rules.query_fermi_data.output
    output:
        # ideal would be to read outputs from url_filenames.txt files but still not sure how because
        # data and spacecraft files change hash at each query so for the same reason not tracked here
        "src/data/Fermi_LAT/gll_psc_v32.xml",
        "src/data/Fermi_LAT/gll_iem_v07.fits",
        "src/data/Fermi_LAT/iso_P8R3_SOURCE_V3_v1.txt",
        "src/data/Fermi_LAT/LAT_extended_sources_14years.tgz",
    conda:
        "environment_fermipy.yml"
    script:
        "src/scripts/download_fermi_data.py"


rule make_evt_list_file:
    input:
        rules.download_fermi_data_files.output,
    output:
        "src/data/Fermi_LAT/evt.list",
    shell:
        "ls $PWD/src/data/Fermi_LAT/*PH*.fits > src/data/Fermi_LAT/evt.list"


rule extract_fermi_extended_source_templates:
    input:
        "src/data/Fermi_LAT/LAT_extended_sources_14years.tgz",
    output:
        directory("src/data/Fermi_LAT/Extended_14years"),
        touch("src/data/extracted_fermi_extended_source_templates.done"),
    shell:
        "tar -xvzf {input[0]} -C src/data/Fermi_LAT"


rule prepare_fermipy_config:
    input:
        "src/scripts/fermipy_config.yml",
        "src/data/Fermi_LAT/evt.list",
    output:
        "src/data/Fermi_LAT/fermipy_config.yml",
    conda:
        "environment.yml"
    script:
        "src/scripts/prepare_fermipy_config.py"

# This is a general rule
# but you can make one for each cube of course
# and put it into a separate directory
rule make_fermipy_ltcube:
    input:
        "src/data/Fermi_LAT/evt.list",
        config = "src/data/Fermi_LAT/fermipy_config.yml",   
    output:
        "src/data/Fermi_LAT/fermipy_analysis/srcmdl_00.xml",
        "src/data/Fermi_LAT/fermipy_analysis/srcmap_00.fits",
        "src/data/Fermi_LAT/fermipy_analysis/ltcube_00.fits",
        "src/data/Fermi_LAT/fermipy_analysis/gtsrcmaps.par",
        "src/data/Fermi_LAT/fermipy_analysis/gtselect.par",
        "src/data/Fermi_LAT/fermipy_analysis/gtltcube.par",
        "src/data/Fermi_LAT/fermipy_analysis/gtexpcube2.par",
        "src/data/Fermi_LAT/fermipy_analysis/gtbin.par",
        "src/data/Fermi_LAT/fermipy_analysis/ft1_00.fits",
        "src/data/Fermi_LAT/fermipy_analysis/evfile_00.txt",
        "src/data/Fermi_LAT/fermipy_analysis/bexpmap_00.fits",
        "src/data/Fermi_LAT/fermipy_analysis/bexpmap_roi_00.fits",
        "src/data/Fermi_LAT/fermipy_analysis/ccube_00.fits",
    conda:
        "environment_fermipy.yml"
    shell:
        "python src/scripts/fermipy_ltcube.py --config {input.config}"


rule run_fermipy_null_hypothesis:
    input:
        "src/data/Fermi_LAT/fermipy_analysis/ltcube_00.fits"
    output:
        "src/data/Fermi_LAT/fermipy_analysis/null_hypothesis.npy",
        "src/data/Fermi_LAT/fermipy_analysis/null_hypothesis_tsmap_output.npy"
    conda:
        "environment_fermipy.yml"
    script:
        "src/scripts/fermipy_null_hypothesis.py"
