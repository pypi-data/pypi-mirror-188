# Copyright (C) 2022 Anthony Harrison
# SPDX-License-Identifier: Apache-2.0

import uuid
from datetime import datetime

from sbom4python.license import LicenseScanner

class CycloneDXGenerator:
    """
    Generate CycloneDX SBOM.
    """

    CYCLONEDX_VERSION = "1.4"
    DATA_LICENCE = "CC0-1.0"
    SPDX_NAMESPACE = "http://spdx.org/spdxdocs/"
    SPDX_LICENCE_VERSION = "3.9"
    SPDX_PROJECT_ID = "SPDXRef-DOCUMENT"
    NAME = "SBOM4PYTHON_Generator"
    PACKAGE_PREAMBLE = "SPDXRef-Package-"
    LICENSE_PREAMBLE = "LicenseRef-"

    def __init__(self, include_license: False, cyclonedx_format="json", application="sbom4python", version="0.1"):
        self.doc = []
        self.package_id = 0
        self.include_license = include_license
        self.license = LicenseScanner()
        self.format = cyclonedx_format
        self.application = application
        self.application_version = version
        if self.format == "xml":
            self.doc = []
        else:
            self.doc = {}
            self.component = []
        self.relationship = []
        self.sbom_complete = False
        self.include_purl = False

    def set_purl(self, package_manager):
        self.include_purl = True
        self.package_manager = package_manager

    def store(self, message):
        self.doc.append(message)

    def getBOM(self):
        if not self.sbom_complete:
            if self.format == "xml":
                self.store("</components>")
                # Now process dependencies
                self.store("<dependencies>")
                for element in self.relationship:
                    item=element["ref"]
                    self.store(f'<dependency ref="{item}">')
                    for depends in element["dependsOn"]:
                        self.store(f'<dependency ref="{depends}"/>')
                    self.store("</dependency>")
                self.store("</dependencies>")
                self.store("</bom>")
            else:
                # Add set of detected components to SBOM
                self.doc["components"] = self.component
                self.doc["dependencies"] = self.relationship
            self.sbom_complete = True
        return self.doc

    def generateTime(self):
        # Generate data/time label in format YYYY-MM-DDThh:mm:ssZ
        return datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

    def generateDocumentHeader(self, project_name):
        if self.format == "xml":
            self.generateXMLDocumentHeader(project_name)
        else:
            self.generateJSONDocumentHeader(project_name)

    def generateJSONDocumentHeader(self, project_name):
        urn = "urn:uuid" + str(uuid.uuid4())
        self.doc = {
            "$schema": "http://cyclonedx.org/schema/bom-1.4.schema.json",
            "bomFormat": "CycloneDX",
            "specVersion": self.CYCLONEDX_VERSION,
            "serialNumber": urn,
            "version": 1,
            "metadata": {
                "timestamp": self.generateTime(),
                "tools": [
                    {
                        "name": self.application,
                        "version": self.application_version,
                    }
                ],
            }
        }

    def generateXMLDocumentHeader(self, project_name):
        urn = "urn:uuid" + str(uuid.uuid4())
        self.store("<?xml version='1.0' encoding='UTF-8'?>")
        self.store("<bom xmlns='http://cyclonedx.org/schema/bom/1.4'")
        self.store(f'serialNumber="{urn}"')
        self.store('version="1">')
        self.store('<metadata>')
        self.store(f'<timestamp>{self.generateTime()}</timestamp>')
        self.store('<tools>')
        self.store(f'<name>{self.application}</name>')
        self.store(f'<version>{self.application_version}</version>')
        self.store('</tools>')
        self.store('</metadata>')
        self.store("<components>")

    def generateRelationship(self, parent_id, package_id):
        # Check if entry exists. If so, update list of dependencies
        element_found = False
        for element in self.relationship:
            if element["ref"] == parent_id:
                # Update list of dependencies
                element["dependsOn"].append(package_id)
                element_found = True
                break
        if not element_found:
            # New item found
            dependency = dict()
            dependency["ref"] = parent_id
            dependency["dependsOn"] = [package_id]
            self.relationship.append(dependency)

    def generateComponent(self, id, type, package):
        if self.format == "xml":
            self.generateXMLComponent(id, type, package)
        else:
            self.generateJSONComponent(id, type, package)

    def generateJSONComponent(self, id, type, package):
        component = dict()
        if "type" in package:
            component["type"] = package["type"]
        else:
            component["type"] = type
        component["bom-ref"] = id
        name = package["name"]
        component["name"] = name
        version = package["version"]
        component["version"] = version
        if "supplier" in package:
            # Depends on supplier type
            if package["supplier_type"] == "Person":
                # Supplier name mustn't have spaces in. Covert spaces to '_'
                component["author"] = package["supplier"].replace(" ", "_")
            else:
                # Organisation is supplier
                ### TODO CHECK
                supplier = dict()
                # Supplier name mustn't have spaces in. Covert spaces to '_'
                supplier["name"] = package["supplier"].replace(" ", "_")
                component["supplier"] = supplier
                component["cpe"] = f'cpe:/a:{supplier["name"]}:{name}:{version}'
                # Alternative is it is within external reference
        if "description" in package:
            component["description"] = package["description"]
        if "checksum" in package:
            for checksum in package["checksum"]:
                checksum_entry = dict()
                checksum_entry["alg"] = checksum[0]
                checksum_entry["content"] = checksum[1]
                if "hashes" in component:
                    component["hashes"].append(checksum_entry)
                else:
                    component["hashes"] = [checksum_entry]
        if "licenseconcluded" in package:
            license_id = self.license.find_license(package["licenseconcluded"])
            # Only include if valid license
            if license_id != "UNKNOWN":
                license = dict()
                license["id"] = license_id
                license_url = self.license.get_license_url(license["id"])
                if license_url is not None:
                    license["url"] = license_url
                item = dict()
                item["license"] = license
                component["licenses"] = [ item ]
        if "copyrighttext" in package:
            component["copyright"] = package["copyrighttext"]
        if "externalreference" in package:
            # Potentially multiple entries
            for reference in package["externalreference"]:
                ref_category = reference[0]
                ref_type = reference[1]
                ref_value = reference[2]
                if ref_category == "SECURITY" and ref_type == "cpe23Type":
                    component["cpe"] = ref_value
                if ref_category == "PACKAGE-MANAGER" and ref_type == "purl":
                    component["purl"] = ref_value
        if "property" in package:
            for property in package["property"]:
                property_entry = dict()
                property_entry["name"] = property[0]
                property_entry["value"] = property[1]
                if "properties" in component:
                    component["properties"].append(property_entry)
                else:
                    component["properties"] = [property_entry]
        self.component.append(component)

    def generateXMLComponent(self, id, type, package):
        self.store(f'<component type="{type}" bom-ref="{id}">')
        name = package["name"]
        version = package["version"]
        self.store(f"<name>{name}</name>")
        self.store(f"<version>{version}</version>")
        if "supplier" in package:
            # Supplier name mustn't have spaces in. Covert spaces to '_'
            self.store(f'<cpe>cpe:/a:{package["supplier"].replace(" ", "_")}:{name}:{version}</cpe>')
        if "licenseconcluded" in package:
            license_id = self.license.find_license(package["licenseconcluded"])
            # Only include if valid license
            if license_id != "UNKNOWN":
                self.store("<licenses>")
                self.store("<license>")
                self.store(f'<id>"{license_id}"</id>')
                license_url = self.license.get_license_url(license_id)
                if license_url is not None:
                    self.store(f'<url>"{license_url}"</url>')
                self.store("</license>")
                self.store("</licenses>")
        if "externalreference" in package:
            # Potentially multiple entries
            for reference in package["externalreference"]:
                ref_category = reference[0]
                ref_type = reference[1]
                ref_value = reference[2]
                if ref_category == "SECURITY" and ref_type == "cpe23Type":
                    self.store(f'<cpe>{ref_value}</cpe>')
                if ref_category == "PACKAGE-MANAGER" and ref_type == "purl":
                    self.store(f"<purl>{ref_value}</purl>")
        self.store("</component>")
