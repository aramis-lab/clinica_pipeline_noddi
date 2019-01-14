# coding: utf8

import clinica.engine as ce


class DwiNoddiCLI(ce.CmdParser):

    def __init__(self):
        super(DwiNoddiCLI, self).__init__()

    def define_name(self):
        """Define the sub-command name to run this pipeline.
        """

        self._name = 'dwi-noddi'

    def define_description(self):
        """Define a description of this pipeline.
        """
        self._description = ('NODDI-based processing of DWI datasets:\n'
                             'https://gitlab.icm-institute.org/aramislab/clinica_pipeline_noddi/tree/master')

    def define_options(self):
        """Define the sub-command arguments
        """

        from clinica.engine.cmdparser import PIPELINE_CATEGORIES

        clinica_comp = self._args.add_argument_group(PIPELINE_CATEGORIES['CLINICA_COMPULSORY'])
        clinica_comp.add_argument("caps_directory",
                                  help='Path to the CAPS directory.')
        clinica_comp.add_argument("list_bvalues", type=str,
                                  help='String listing all the shells (i.e. the b-values) in the corrected DWI datasets comma separated (e.g, 0,300,700,2200)')
        # Optional arguments
        clinica_opt = self._args.add_argument_group(PIPELINE_CATEGORIES['CLINICA_OPTIONAL'])

        clinica_opt.add_argument("-wd", "--working_directory",
                                 help='Temporary directory to store pipeline intermediate results')
        clinica_opt.add_argument("-np", "--n_procs", type=int, default=4,
                                 help='Number of cores used to run in parallel')
        clinica_opt.add_argument("-tsv", "--subjects_sessions_tsv",
                                 help='TSV file containing a list of subjects with their sessions.')

    def run_command(self, args):
        """
        """
        import os
        from tempfile import mkdtemp
        from clinica.utils.stream import cprint
        from clinica.pipelines.dwi_noddi.dwi_noddi_pipeline import DwiNoddi

        pipeline = DwiNoddi(
            caps_directory=self.absolute_path(args.caps_directory),
            tsv_file=self.absolute_path(args.subjects_sessions_tsv)
        )

        # Check NODDI Matlab toolbox:
        try:
            noddi_matlab_toolbox = os.environ.get('NODDI_MATLAB_TOOLBOX', '')
            if not noddi_matlab_toolbox:
                raise RuntimeError('NODDI_MATLAB_TOOLBOX variable is not set')
        except Exception as e:
            cprint(str(e))
        cprint('NODDI Matlab toolbox has been detected')

        # Check Niftimatlib toolbox.
        try:
            nifti_matlib_toolbox = os.environ.get('NIFTI_MATLIB_TOOLBOX', '')
            if not nifti_matlib_toolbox:
                raise RuntimeError('NIFTI_MATLIB_TOOLBOX variable is not set')
        except Exception as e:
            cprint(str(e))
        cprint('Niftimatlib toolbox has been detected')

        pipeline.parameters = {
            'bvalue_str': dict([
                ('bvalue_str', args.list_bvalues)
            ]),
            'n_procs': dict([
                ('n_procs', args.n_procs or 4)]
            ),
            'noddi_toolbox_dir': dict([
                ('noddi_toolbox_dir', noddi_matlab_toolbox)]
            ),
            'nifti_matlib_dir': dict([
                ('nifti_matlib_dir', nifti_matlib_toolbox)
            ]),
        }

        if args.working_directory is None:
            args.working_directory = mkdtemp()
        pipeline.base_dir = self.absolute_path(args.working_directory)
        if args.n_procs:
            pipeline.run(plugin='MultiProc',
                         plugin_args={'n_procs': args.n_procs})
        else:
            pipeline.run()
