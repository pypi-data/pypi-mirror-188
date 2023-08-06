from enum import Enum, unique


@unique
class ConstituentOverrideMode(Enum):
    MERGE_WITH_DEFINITION = "MergeWithDefinition"
    REPLACE_DEFINITION = "ReplaceDefinition"
