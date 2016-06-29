# Copyright (c) 2013 Shotgun Software Inc.
# 
# CONFIDENTIAL AND PROPRIETARY
# 
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit 
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your 
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights 
# not expressly granted therein are reserved by Shotgun Software Inc.

"""
An app that loads materials based on the vrayproxy paths.

"""

import sys
import os
from tank.platform import Application
from tank.platform.qt import QtCore, QtGui
import tank



class AutoLoadScene(Application):

    def init_app(self):
        """
        App entry point
        """
        # make sure that the context has an entity associated - otherwise it wont work!
        if self.context.entity is None:
            raise tank.TankError("Cannot load the AutoLoadScene application! "
                                 "Your current context does not have an entity (e.g. "
                                 "a current Shot, current Asset etc). This app requires "
                                 "an entity as part of the context in order to work.")

        app_name = self.get_setting("display_name")

        available_steps = self.get_setting("available_steps")

        if self.context.step['name'] in available_steps:

            self.engine.register_command(app_name, self.run_app)

    def destroy_app(self):
        """
        App teardown
        """
        self.log_debug("Destroying sg_auto_scene_loader")


    def run_app(self):
        """
        Callback from when the menu is clicked.
        """

        shotgun_filters = self.replace_filters_tokens(self.get_setting("sg_filters"))

        import pprint
        pprint.pprint(shotgun_filters)

        shotgun_order = self.get_setting("sg_order")

        publish_fields_dict = self.shotgun.schema_field_read("PublishedFile")

        shotgun_fields = []

        for field in publish_fields_dict:
            shotgun_fields.append(field)

        published_file = self.shotgun.find_one("PublishedFile", shotgun_filters, shotgun_fields, order=shotgun_order)

        if published_file:

            self.log_debug("Found published_file with id: %s" % published_file["id"])

            published_file_path = published_file["path"]["local_path"]

            hook_result = self.execute_hook("pre_load_hook", sg_publish_data = published_file)

            hook_result = self.execute_hook("load_hook", path = published_file_path, sg_publish_data = published_file)

            hook_result = self.execute_hook("post_load_hook", sg_publish_data = published_file)

        else:

            self.log_debug("Cant found a valid scene file for your current context!")



    def replace_filters_tokens(self, filters):

        new_filters = []

        for sfilter in filters:

            new_elements = []

            for element in sfilter:

                new_element = self.match_filter_element(element)

                new_elements.append(new_element)

            new_filters.append(new_elements)

        return new_filters



    def match_filter_element(self, element):

        if element == "{context_entity}":

            return self.context.entity

        elif element == "{context_step}":

            return self.context.step

        elif element == "{context_project}":

            return self.context.project

        elif element == "{context_step}":

            return self.context.step

        elif element == "{context_user}":

            return self.context.user

        else:

            return element