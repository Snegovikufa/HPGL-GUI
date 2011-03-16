from distutils.core import setup
from distutils.dir_util import copy_tree
from py2exe.build_exe import py2exe
import glob
import os
import zlib
import shutil
import time
import shutil
import enthought.tvtk
import enthought.mayavi
import enthought.chaco
import geo_bsd
import vtk

distDir = "HPGL-GUI-builded"

# Remove the build folder
shutil.rmtree("build", ignore_errors=True)
#shutil.rmtree("ufsim-office-builded", ignore_errors=True)

class Target(object):
    """ A simple class that holds information on our executable file. """
    def __init__(self, **kw):
        """ Default class constructor. Update as you need. """
        self.__dict__.update(kw)
        

geoPath = os.path.join( distDir, "geo_bsd")
copy_tree(geo_bsd.__path__[0], geoPath)

resourcesPath = os.path.join( distDir, "icons")
copy_tree("icons", resourcesPath)

tvtkPath = os.path.join( os.path.join(distDir, "enthought"), "tvtk")
copy_tree(enthought.tvtk.__path__[0], tvtkPath )

mayaviPath = os.path.join( os.path.join(distDir, "enthought"), "mayavi")
copy_tree(enthought.mayavi.__path__[0], mayaviPath )

chacoPath = os.path.join( os.path.join(distDir, "enthought"), "chaco")
copy_tree(enthought.chaco.__path__[0], chacoPath )

vtkPath = os.path.join( distDir, "vtk")
copy_tree(vtk.__path__[0], vtkPath )

includes = [ 'sip', 'PySide.QtGui', 'PySide.QtCore', 'PySide.QtNetwork', 
            'enthought', 
            #'vtk', 
            ]
excludes = ['_gtkagg', '_tkagg', 'bsddb', 'curses', 'email', 'pywin.debugger',
            'pywin.debugger.dbgcon', 'pywin.dialogs', 'tcl',
            'Tkconstants', 'Tkinter']
            
packages = ['enthought', 'vtk']

dll_excludes = ['libgdk-win32-2.0-0.dll', 'libgobject-2.0-0.dll', 'tcl84.dll',
                'tk84.dll']

data_files = []
icon_resources = [(1, "hpgl-gui.ico")]
bitmap_resources = []
other_resources = []


GUI2Exe_Target_1 = Target(
    # what to build
    script = "gui.py",
    icon_resources = icon_resources,
    bitmap_resources = bitmap_resources,
    other_resources = other_resources,
    dest_base = "hpgl-gui",    
    version = "0.9",
    company_name = "MIT Ufa",
    copyright = "MIT Ufa",
    name = "HPGL GUI",
    
    )

                    
setup(

    data_files = data_files,

    options = {"py2exe": {"compressed": 0, 
                          "optimize": 0,
                          "includes": includes,
                          "excludes": excludes,
                          "packages": packages,
                          "dll_excludes": dll_excludes,
                          "bundle_files": 3,
                          "dist_dir": distDir,
                          "xref": False,
                          "skip_archive": True,
                          "ascii": False,
                          "custom_boot_script": '',
                         }
              },

    zipfile = r'library.zip',
    console = [],
    windows = [GUI2Exe_Target_1],
    service = [],
    com_server = [],
    ctypes_com_server = []
    )
