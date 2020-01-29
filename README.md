This repository contains the NODDI pipeline and preprocessing pipeline for multi-shell data used for the paper "Neurite density is reduced in the presymptomatic phase of C9orf72 disease".

These pipelines need the [Clinica software platform](http://www.clinica.run) that you will have to install.

If you use these pipelines, please cite:
> J. Wen, H. Zhang, D. C Alexander, S. Durrleman, A. Routier, D. Rinaldi, M. Houot, P. Couratier, D. Hannequin, F. Pasquier, J. Zhang, O. Colliot, I. Le Ber and A. Bertrand **Neurite density is reduced in the presymptomatic phase of C9orf72 disease** *Journal of Neurology, Neurosurgery, and Psychiatry, 2018*.

As well as neuroimagning tools behind these pipelines.

 :warning: **Please note that this repository is not maintained anymore** :warning:

Original author: Junhao Wen ([@anbai106](https://github.com/anbai106/))

## How to use this repo?
- Follow the [developper installation of Clinica](http://www.clinica.run/doc/Installation/) and install v0.2.X version (e.g. `git checkout v0.2.0` before `conda env create -f environment.yml`)
- Clone this repo
- Create the environment variable `CLINICAPATH` like this:
```bash
export CLINICAPATH="/path/to/the/repo/clinica_pipeline_noddi"
```

When typing `clinica run` in your terminal, you should see `dwi-preprocessing-multi-shell` and `dwi-noddi` pipelines.




## `dwi-noddi` – NODDI-based processing of multi-shell datasets

The `dwi-noddi` pipeline computes the Neurite Orientation Dispersion and Density Imaging (NODDI) model from multi-shell datasets with extraction of NODDI-based measures namely the neurite density index (NDI), the orientation dispersion index (ODI) ant the free water fraction (FWF).

Then, normalization of the NODDI-derived scalar maps (NDI, ODI, FWF) onto an FA-atlas with labelled tracts, and generation of TSV files containing a summary of the regional statistics (mean NODDI-based measures) to ease subsequent statistical analyses.

To that aim, it mainly relies on the **NODDI Matlab Toolbox** [[Zhang et al., 2012]](http://dx.doi.org/10.1016/j.neuroimage.2012.03.072) for NODDI aspects and on **ANTs** for the normalization aspects [[Avants et al., 2008](https://doi.org/10.1016/j.media.2007.06.004)].


### Prerequisites
You need [preprocessed DWI data](../DWI_Preprocessing) prior to running any of these pipelines.

!!! note "Notes concerning the `dwi-preprocessing-multi-shell` pipeline"
    The `dwi-preprocessing-multi-shell` does not currently read parameters from JSON files, you need to provide them on the command line.



### Dependencies

If you only installed the core of Clinica, this pipeline needs the installation of **ANTs**,  **FSL** and **NODDI Matlab Toolbox** on your computer if you want to run the `dwi-noddi` pipeline. You can find how to install these software packages on the [third-party](http://www.clinica.run/doc/Third-party/) page.

>**Note:**
>
> In order to use the interaction between the NODDI Matlab Toolbox and Clinica, we defined the `NODDI_MATLAB_TOOLBOX` environment variable as well as the `NIFTI_MATLAB_TOOLBOX` environment variable (niftimatlib is a dependency of NODDI Matlab Toolbox).

### Running the pipeline
The `dwi-noddi` pipeline can be run with the following command line:

```
clinica run dwi-noddi caps_directory
```

where:

  - `caps_directory` is the input/output folder containing the results in a [CAPS](../CAPS) hierarchy.

If you want to run the pipeline on a subset of your CAPS dataset, you can use the `-tsv` flag to specify in a TSV file the participants belonging to your subset.


### Outputs

Results are stored in the following folder of the [CAPS hierarchy](../CAPS): `subjects/sub-<participant_label>/ses-<session_label>/dwi/noddi_based_processing/`.

The main output files are:

- native_space/:
    - `<source_file>_space-[b0|T1w]_model-NODDI_diffmodel.nii.gz`: The Neurite Orientation Dispersion and Density Imaging (NODDI) data of the subject.
    - `<source_file>_space-[b0|T1w]_[FWF|NDI|ODI].nii.gz`: The NODDI-based measures, namely namely the neurite density index (`NDI`), the orientation dispersion index (`ODI`) ant the free water fraction (`FWF`).
- normalized_space/
    - `<source_file>_space-<space>_[FWF|NDI|ODI].nii.gz`: The NODDI-based measures registered to the space of an FA-atlas.
- atlas_statistics/
    - `<source_file>_space-<space>_map-[FWF|NDI|ODI]_statistics.tsv`: TSV files summarizing the regional statistics on the labelled atlas `<space>`.


> **Note:** Atlases available for the NODDI-based processing pipeline:
> - [JHUDTI81](http://www.loni.usc.edu/ICBM/Downloads/Downloads_DTI-81.shtml) [[Hua et al., 2008](https://doi.org/10.1016/j.neuroimage.2007.07.053); [Wakana et al., 2007](https://doi.org/10.1016/j.neuroimage.2007.02.049)]: This atlas contains 48 white matter tract labels that were created by manually segmenting a standard-space average of diffusion MRI tensor maps from 81 subjects.
> - [JHUTracts[0|25|50]](https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/Atlases) [Mori et al., 2005]. This atlas contains 20 white matter tract labels that were identified probabilistically by averaging the results of deterministic tractography run on 28 subjects. Several thresholds of these probabilistic tracts are proposed (0%, 25%, 50%).
