# Copyright (C) 2022 Anthony Harrison
# SPDX-License-Identifier: Apache-2.0

import json
import re

import defusedxml.ElementTree as ET
import yaml

from lib4sbom.package import SBOMPackage
from lib4sbom.file import SBOMFile


class SPDXParser:
    def __init__(self):
        pass

    def parse(self, sbom_file):
        """parses SPDX SBOM file"""
        if sbom_file.endswith(".spdx"):
            return self.parse_spdx_tag(sbom_file)
        elif sbom_file.endswith(".spdx.json"):
            return self.parse_spdx_json(sbom_file)
        elif sbom_file.endswith(".spdx.rdf"):
            return self.parse_spdx_rdf(sbom_file)
        elif sbom_file.endswith(".spdx.xml"):
            return self.parse_spdx_xml(sbom_file)
        elif sbom_file.endswith((".spdx.yaml", "spdx.yml")):
            return self.parse_spdx_yaml(sbom_file)
        else:
            return {}, {}

    def parse_spdx_tag(self, sbom_file):
        """parses SPDX tag value SBOM file extracting package name, version and license and other data"""
        with open(sbom_file) as f:
            lines = f.readlines()
        packages = {}
        spdx_package = SBOMPackage()
        files = {}
        spdx_file = SBOMFile()
        spdx_file.initialise()
        spdx_package.initialise()
        package = None
        file = None
        for line in lines:
            line_elements = line.split(":")
            # TODO File handling
            if line_elements[0] == "FileName":
                # Is this a new file?
                if file is not None and file not in files:
                    # Save file metadata
                    files[file] = spdx_file.get_file()
                file = line_elements[1].strip().rstrip("\n")
                # Reset all variables
                spdx_file.initialise()
                spdx_file.set_name(file)
            elif line_elements[0] == "FileType":
                filetype = line_elements[1].strip().rstrip("\n")
                spdx_file.set_filetype (filetype)
            elif line_elements[0] == "FileChecksum":
                checksum_type = line_elements[1]
                checksum = line_elements[2].strip().rstrip("\n")
                spdx_file.set_checksum(checksum_type, checksum)
            elif line_elements[0] == "LicenseConcluded":
                license_concluded = line_elements[1].strip().rstrip("\n")
                spdx_file.set_licenseconcluded (license_concluded )
            elif line_elements[0] == "LicenseInfoInFile":
                license_info= line_elements[1].strip().rstrip("\n")
                spdx_file.set_licenseinfoinfile(license_info)
            elif line_elements[0] == "LicenseComments":
                license_info= line_elements[1].strip().rstrip("\n")
                spdx_file.set_licensecomment(license_info)
            elif line_elements[0] == "FileCopyrightText":
                copyright_text = line_elements[1].strip().rstrip("\n")
                spdx_file.set_copyrighttext(copyright_text)
            elif line_elements[0] == "FileComment":
                comment_text = line_elements[1].strip().rstrip("\n")
                spdx_file.set_comment(comment_text)
            elif line_elements[0] == "FileNotice":
                note = line_elements[1].strip().rstrip("\n")
                spdx_file.set_notice(note)
            elif line_elements[0] == "FileAttributionText":
                attribution = line_elements[1].strip().rstrip("\n")
                spdx_file.set_attribution(attribution)

            if line_elements[0] == "PackageName":
                # Is this a new package?
                if package is not None and package not in packages:
                    # Save package metadata
                    packages[package] = spdx_package.get_package()
                package = line_elements[1].strip().rstrip("\n")
                # Reset all variables
                spdx_package.initialise()
                spdx_package.set_name(package)
                # Default type of component
                spdx_package.set_type("library")
            elif line_elements[0] == "PackageVersion":
                version = line_elements[1].strip().rstrip("\n")
                version = version.split("-")[0]
                version = version.split("+")[0]
                spdx_package.set_version(version)
            elif line_elements[0] == "PackageFileName":
                filename = line_elements[1].strip().rstrip("\n")
                spdx_package.set_filename(filename)
            elif line_elements[0] == "PackageSupplier":
                supplier_type = line_elements[1]
                supplier = line_elements[2].strip().rstrip("\n")
                spdx_package.set_supplier(supplier_type, supplier)
            elif line_elements[0] == "PackageOriginator":
                originator_type = line_elements[1]
                originator = line_elements[2].strip().rstrip("\n")
                spdx_package.set_originator(originator_type, originator)
            elif line_elements[0] == "PackageDownloadLocation":
                downloadlocation = line[24:].strip().rstrip("\n")
                spdx_package.set_downloadlocation(downloadlocation)
            elif line_elements[0] == "FilesAnalyzed":
                file_analysis = line_elements[1].strip().rstrip("\n")
                spdx_package.set_filesanalysis(file_analysis)
            elif line_elements[0] == "PackageChecksum":
                checksum_type = line_elements[1]
                checksum = line_elements[2].strip().rstrip("\n")
                spdx_package.set_checksum(checksum_type, checksum)
            elif line_elements[0] == "PackageHomePage":
                homepage = line[17:].strip().rstrip("\n")
                spdx_package.set_homepage(homepage)
            elif line_elements[0] == "PackageSourceInfo":
                sourceinfo= line[17:].strip().rstrip("\n")
                spdx_package.set_soureinfo(sourceinfo)
            elif line_elements[0] == "PackageLicenseConcluded":
                license_concluded = line_elements[1].strip().rstrip("\n")
                spdx_package.set_licenseconcluded (license_concluded )
            elif line_elements[0] == "PackageLicenseDeclared":
                license_declared = line_elements[1].strip().rstrip("\n")
                spdx_package.set_licensedeclared (license_declared )
            elif line_elements[0] == "PackageLicenseComments":
                license_comments= line_elements[1].strip().rstrip("\n")
                spdx_package.set_licensecomments(license_comments)
            elif line_elements[0] == "PackageLicenseInfoFromFiles":
                license_info= line_elements[1].strip().rstrip("\n")
                spdx_package.set_licenseinfoinfiles(license_info)
            elif line_elements[0] == "PackageLicenseCopyrightTest":
                copyright_text = line_elements[1].strip().rstrip("\n")
                spdx_package.set_copyrighttext(copyright_text)
            elif line_elements[0] == "PackageComment":
                comments = line_elements[1].strip().rstrip("\n")
                spdx_package.set_comment(comments)
            elif line_elements[0] == "PackageSummary":
                summary = line_elements[1].strip().rstrip("\n")
                spdx_package.set_summary (summary)
            elif line_elements[0] == "PackageDescription":
                description = line_elements[1].strip().rstrip("\n")
                spdx_package.set_description (description)
            elif line_elements[0] == "ExternalRef":
                # Format is TAG CATEGORY TYPE LOCATOR
                # Need all data after type which may contain :. Therefore capture all data after Tag
                ext_elements = line.split("ExternalRef:",1)[1].strip().rstrip("\n")
                ref_category = ext_elements.split()[0]
                ref_type = ext_elements.split()[1]
                ref_locator = ext_elements.split()[2]
                spdx_package.set_externalreference(ref_category, ref_type, ref_locator)
            elif line_elements[0] == "Relationship":
                # TODO Decide what to do!!
                pass
        # Save last package/file
        if file is not None and file not in files:
            # Save file metadata
            files[file] = spdx_file.get_file()
        if package is not None and package not in packages:
            # Save package metadata
            packages[package] = spdx_package.get_package()
        return files, packages

    def parse_spdx_json(self, sbom_file):
        """parses SPDX JSON SBOM file extracting package name, version, license and other data"""
        data = json.load(open(sbom_file))
        packages = {}
        spdx_package = SBOMPackage()
        files = {}
        spdx_file = SBOMFile()
        for d in data["files"]:
            spdx_file.initialise()
            filename = d["fileName"]
            spdx_file.set_name(filename)
            try:
                if "checksum" in d:
                    # Potentially multiple entries
                    for checksum in d["checksum"]:
                         spdx_file.set_checksum(checksum["algorithm"], checksum["checkumValue"])
                if "licenseConcluded" in d:
                    spdx_file.set_licenseconcluded(d["licenseConcluded"])
                if "copyrightText" in d:
                    spdx_file.set_copyrighttext(d["copyrightText"])
                if filename not in files:
                    # Save file metadata
                    files[filename] = spdx_file.get_file()
            except KeyError as e:
                print (f"Unable to store file info: {filename}")
                pass

        for d in data["packages"]:
            spdx_package.initialise()
            package = d["name"]
            spdx_package.set_name(package)
            # Default type of component
            spdx_package.set_type("library")
            try:
                version = d["versionInfo"]
                spdx_package.set_version(version)
                if "supplier" in d:
                    supplier=d["supplier"].split(":")
                    spdx_package.set_supplier(supplier[0],supplier[1])
                if "originator" in d:
                    originator = d["originator"].split(":")
                    spdx_package.set_originator(originator[0], originator[1])
                if "filesAnaylzed" in d:
                    spdx_package.set_filesAnalyzed(d["filesAnaylzed"])
                if "filename" in d:
                    spdx_package.set_fileName(d["filename"])
                if "homepage" in d:
                    spdx_package.set_homepage(d["homepage"])
                if "checksum" in d:
                    # Potentially multiple entries
                    for checksum in d["checksum"]:
                         spdx_package.set_checksum(checksum["algorithm"], checksum["checkumValue"])
                if "sourceinfo" in d:
                    spdx_package.set_sourceInfo(d["sourceinfo"])
                if "licenseConcluded" in d:
                    spdx_package.set_licenseconcluded(d["licenseConcluded"])
                if "licenseDeclared" in d:
                    spdx_package.set_licensedeclared(d["licenseDeclared"])
                if "licenseComments" in d:
                    spdx_package.set_licensecomments(d["licenseComments"])
                if "copyrightText" in d:
                    spdx_package.set_copyrighttext(d["copyrightText"])
                if "downloadLocation" in d:
                    spdx_package.set_downloadlocation(d["downloadLocation"])
                if "description" in d:
                    spdx_package.set_description(d["description"])
                if "comment" in d:
                    spdx_package.set_comment(d["comment"])
                if "summary" in d:
                    spdx_package.set_summary(d["summary"])
                if "downloadlocation" in d:
                    spdx_package.set_downloadlocation(d["downloadlocation"])
                if "externalRefs" in d:
                    for ext_ref in d["externalRefs"]:
                        spdx_package.set_externalreference(ext_ref["referenceCategory"], ext_ref["referenceType"],ext_ref["referenceLocator"])
                if package not in packages:
                    # Save package metadata
                    packages[package] = spdx_package.get_package()

            except KeyError as e:
                print (f"Unable to store package info: {package}")
                pass

        return files, packages

    def parse_spdx_rdf(self, sbom_file):
        """parses SPDX RDF SBOM file extracting package name, version, license and other data"""
        with open(sbom_file) as f:
            lines = f.readlines()
        files = {}
        packages = {}
        package = ""
        for line in lines:
            try:
                if line.strip().startswith("<spdx:name>"):
                    stripped_line = line.strip().rstrip("\n")
                    package_match = re.search(
                        "<spdx:name>(.+?)</spdx:name>", stripped_line
                    )
                    if not package_match:
                        raise KeyError(f"Could not find package in {stripped_line}")
                    package = package_match.group(1)
                    version = None
                elif line.strip().startswith("<spdx:versionInfo>"):
                    stripped_line = line.strip().rstrip("\n")
                    version_match = re.search(
                        "<spdx:versionInfo>(.+?)</spdx:versionInfo>", stripped_line
                    )
                    if not version_match:
                        raise KeyError(f"Could not find version in {stripped_line}")
                    version = version_match.group(1)
                    # To handle case where license appears before version
                    if package not in packages and license is not None:
                        packages[package] = [version, license]
                        version = None
                elif line.strip().startswith("<spdx:licenseConcluded"):
                    stripped_line = line.strip().rstrip("\n")
                    # Assume license tag is on a single line
                    license_match = re.search(
                        "<spdx:licenseConcluded rdf:resource=(.+?)/>", stripped_line
                    )
                    if license_match is None:
                        license = "NOT FOUND"
                    else:
                        license = license_match.group(1)
                        if license.startswith("\"http://spdx.org/licenses/"):
                            # SPDX license identifier. Extract last part of url
                            license = license.split("/")[-1]
                            license=license[:-1] # Remove trialing "
                        if "#" in license:
                            # Extract last part of url after # e.g. http://spdx.org/rdf/terms#noassertion
                            license = license.split("#")[-1]
                            license=license[:-1].upper() # Remove trialing " and capitalise
                    # To handle case where license appears before version
                    if package not in packages and version is not None:
                        packages[package] = [version, license]
                        license = None
            except KeyError as e:
                pass

        return files, packages

    def parse_spdx_yaml(self, sbom_file):
        """parses SPDX YAML SBOM file extracting package name, version, license and other data"""
        data = yaml.safe_load(open(sbom_file))
        files = {}
        packages = {}
        for d in data["packages"]:
            package = d["name"]
            try:
                version = d["versionInfo"]
                license = d["licenseConcluded"]
                if package not in packages:
                    packages[package] = [version, license]
            except KeyError as e:
                pass

        return files, packages

    def parse_spdx_xml(self, sbom_file):
        """parses SPDX XML SBOM file extracting package name, version, license and other data"""
        # XML is experimental in SPDX 2.3
        files = {}
        packages = {}
        tree = ET.parse(sbom_file)
        # Find root element
        root = tree.getroot()
        # Extract schema
        schema = root.tag[: root.tag.find("}") + 1]

        for component in root.findall(schema + "packages"):
            try:
                package_match = component.find(schema + "name")
                if package_match is None:
                    raise KeyError(f"Could not find package in {component}")
                package = package_match.text
                if package is None:
                    raise KeyError(f"Could not find package in {component}")
                version_match = component.find(schema + "versionInfo")
                if version_match is None:
                    raise KeyError(f"Could not find version in {component}")
                version = version_match.text
                if version is None:
                    raise KeyError(f"Could not find version in {component}")
                component_license = component.find(schema + "licenseConcluded")
                if component_license is None:
                    license = "NOT FOUND"
                else:
                    license = component_license.text

                if version is not None:
                    if package not in packages:
                        packages[package] = [version, license]

            except KeyError as e:
                pass

        return files, packages
