# Copyright (C) 2023 Anthony Harrison
# SPDX-License-Identifier: Apache-2.0

from typing import List, NamedTuple, Dict

class SBOMData(NamedTuple):
    document: List
    files: Dict
    packages: Dict
    relationships: List
    type : str
    version : str

