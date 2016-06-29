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


class PreLoadHook(Hook):
    """
    Hook to setup this before loading
    """
    def execute(self, sg_publish_data, **kwargs):
        """
        Process current engine and scene settings before loading the new scene contents.
        
        :param sg_publish_data: Shotgun data dictionary with all the standard publish fields.
        """

        self.parent.log_debug("Executing PreLoadHook")