# Copyright (C) 2023 Anthony Harrison
# SPDX-License-Identifier: Apache-2.0

### Example to show use of lib4sbom to parse a SBOM and
### produce a summary of its contents against NTIA minimum elements

import sys
from lib4sbom.parser import SBOMParser
from lib4sbom.data.document import SBOMDocument


test_parser = SBOMParser()
# Load SBOM
test_parser.parse_file(sys.argv[1])
# What type of SBOM
document = SBOMDocument()
document.copy_document(test_parser.get_document())

packages = test_parser.get_packages()
files = test_parser.get_files()
relationships = test_parser.get_relationships()

print ("SBOM Summary")
print ("=" * len("SBOM Summary"))
print (f"SBOM File     {sys.argv[1]}")
print (f"SBOM Type     {document.get_type()}")
print (f"Version       {document.get_version()}")
print (f"Name          {document.get_name()}")
creator_identified = False
for c in document.get_creator():
    creator_identified = True
    print (f"Creator       {c[0]} {c[1]}")
creation_time = (document.get_created() is not None)
print (f"Created       {document.get_created()}")
print (f"Files         {len(files)}")
print (f"Packages      {len(packages)}")
print (f"Relationships {len(relationships)}")
files_valid = True
packages_valid = True
relationships_valid = (len(relationships) > 0)
sbom_licenses = []
for file in files:
    # Minimum elements are ID, Name
    id = file.get('id', None)
    name = file.get('name', None)
    license = file.get('licenseconcluded', None)
    if license is not None:
        sbom_licenses.append(license)
    if id is None or name is None:
        files_valid = False

for package in packages:
    # Minimum elements are ID, Name, Version, Supplier
    id = package.get('id', None)
    name = package.get('name', None)
    version = package.get('version', None)
    supplier = package.get('supplier', None)
    license = package.get('licenseconcluded', None)
    if license is not None:
        sbom_licenses.append(license)
    if id is None or name is None or version is None or supplier is None:
        packages_valid = False

print ("\nNTIA Summary")
print ("=" * len("NTIA Summary"))
print (f"\n{'Element':40} Status")
print ("-" * 50)
print (f"{'All file information provided?':40} {files_valid}")
print (f"{'All package information provided?':40} {packages_valid}")
print (f"{'Creator identified?':40} {creator_identified}")
print (f"{'Creation time identified?':40} {creation_time}")
print (f"{'Dependency relationships provided?':40} {relationships_valid}")
valid_sbom = (files_valid and packages_valid and creator_identified and creation_time and relationships_valid)
print (f"\nNTIA conformant {valid_sbom}")

print ("\nLicense Summary")
print ("=" * len("License Summary"))
print (f"\n{'License':40} Count")
print ("-" * 50)
# Create an empty dictionary
freq = {}
for items in sbom_licenses:
    freq[items] = sbom_licenses.count(items)
for key, value in freq.items():
    print(f"{key:40} {value}")
