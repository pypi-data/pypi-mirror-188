# Copyright (C) 2022 Anthony Harrison
# SPDX-License-Identifier: Apache-2.0

class SBOMRelationship:

    def __init__(self):
        pass

    def initialise(self):
        self.relationship = {}

    def set_name(self, name):
        self.relationship["name"] = name

    def get_relationship(self):
        return self.relationship

    def debug_relationship(self):
        print ("OUTPUT:", self.relationship)

    def show_relationship(self):
        for key in self.relationship:
            print (f"{key}    : {self.relationship[key]}")

    def copy_relationship(self, relationship_info):
        for key in relationship_info:
            self.set_value(key, relationship_info[key])

    def get_name(self):
        return self.relationship["name"]