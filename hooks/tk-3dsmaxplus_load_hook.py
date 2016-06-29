# Copyright (c) 2013 Shotgun Software Inc.
# 
# CONFIDENTIAL AND PROPRIETARY
# 
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit 
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your 
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights 
# not expressly granted therein are reserved by Shotgun Software Inc.

import os
import MaxPlus

import tank
from tank import Hook
from tank import TankError


class LoadHook(Hook):
    """
    Hook to load scene
    """
    def execute(self, path, sg_publish_data, **kwargs):
        """
        Merge contents of the given file into the scene.
        
        :param path: Path to file.
        :param sg_publish_data: Shotgun data dictionary with all the standard publish fields.
        """

        self.parent.log_debug("Executing LoadHook for path %s" % path)


        if not os.path.exists(path):
            raise Exception("File not found on disk - '%s'" % path)
        
        (_, ext) = os.path.splitext(path)
        
        supported_file_exts = [".max"]
        if ext.lower() not in supported_file_exts:
            raise Exception("Unsupported file extension for '%s'. "
                            "Supported file extensions are: %s" % (path, supported_file_exts))

        MaxPlus.Core.EvalMAXScript('mergeMAXFile(\"' + path.replace('\\', '/') + '\")')