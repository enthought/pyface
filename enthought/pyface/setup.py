#!/usr/bin/env python

import os.path

minimum_numpy_version = '0.9.7.2467'
def configuration(parent_package='enthought',top_path=None):
    import numpy
    if numpy.__version__ < minimum_numpy_version:
        raise RuntimeError, 'numpy version %s or higher required, but got %s'\
              % (minimum_numpy_version, numpy.__version__)

    from numpy.distutils.misc_util import Configuration
    config = Configuration('pyface',parent_package,top_path)
    config.set_options(ignore_setup_xxx_py=True,
                       assume_default_configuration=True,
                       delegate_options_to_subpackages=True,
                       quiet=True)

    #add the parent __init__.py to allow for importing
    config.add_data_files(('..', os.path.abspath(os.path.join('..','__init__.py'))))
    
    #add version info for use in the about dialog
    config.add_data_files(('..', os.path.abspath(os.path.join('..','version.py'))))
    if os.path.exists(os.path.join('..','__svn_version__.py')):
        config.add_data_files(('..', os.path.abspath(os.path.join('..','__svn_version__.py'))))

    config.add_subpackage('action')
    config.add_subpackage('dock')
    config.add_subpackage('examples')
    config.add_subpackage('grid')
    config.add_subpackage('preference')
    config.add_subpackage('sheet')
    config.add_subpackage('sizers')
    config.add_subpackage('tree')
    config.add_subpackage('util')
    config.add_subpackage('viewer')
    config.add_subpackage('wizard')

    config.add_data_dir('action/images')
    config.add_data_dir('doc')
    config.add_data_dir('dock/demos')
    config.add_data_dir('dock/images')
    config.add_data_dir('dock/features')
    config.add_data_dir('examples')
    config.add_data_dir('grid/images')
    config.add_data_dir('grid/tests')
    config.add_data_dir('images')
    config.add_data_dir('sheet/tests')
    config.add_data_dir('sheet/swig_interface')
    config.add_data_dir('tree/images')
    
    return config

if __name__ == "__main__":
    from numpy.distutils.core import setup
    setup(version='1.1.1',
           description      = 'Traits capable windowing framework',
           author           = 'Enthought, Inc',
           author_email     = 'info@enthought.com',
           url              = 'http://code.enthought.com/ets',
           license          = 'BSD',
           install_requires = ["enthought.naming", "enthought.logger", "enthought.debug"],
           extras_require   = { "tvtk" : ["enthought.pyface.tvtk"] },
           zip_safe     = False, # needed for Traits
           configuration    = configuration)
