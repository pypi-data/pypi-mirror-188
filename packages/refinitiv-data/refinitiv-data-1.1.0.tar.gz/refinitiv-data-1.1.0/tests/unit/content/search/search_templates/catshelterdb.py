"""Module with 'in-memory Database' based on pandas, with several tables.

Goal is to replace discovery search templates API in target templates testing without
need to emulate it, patch objects, etc..
Almost everything can be tested that way. Because all logic of TargetTemplate is not
tied to search template API.
"""

from typing import Optional

import pandas as pd

from refinitiv.data.discovery._search_templates.base import Target

__all__ = ["CatsDatabaseTarget"]

DB = {
    "cats": pd.DataFrame(
        columns=("name", "age", "gender", "breed", "shelter"),
        data=[
            ("Richard", 12, "male", "Birman", "01"),
            ("Bear", 9, "male", "Sphynx", "02"),
            ("Thomas", 25, "male", "Birman", "01"),
            ("Maverick", 19, "male", "Munchkin", "03"),
            ("Einstein", 21, "male", "Ragdoll", "03"),
            ("Athena", 8, "female", "Sphynx", "02"),
            ("Rita", 12, "female", "Birman", "01"),
            ("Luna", 16, "female", "Ragdoll", "01"),
            ("Elsa", 32, "female", "Munchkin", "02"),
            ("Maeve", 19, "female", "Bombay", "02"),
        ],
    ),
    "breeds": pd.DataFrame(
        columns=("name", "origin", "body_type", "coat"),
        data=[
            ("Birman", "France", "cobby", "semi-long"),
            ("Sphynx", "Canada,Europe", "oriental", "hairless"),
            ("Bombay", "US,Burma", "cobby", "short"),
            ("Munchkin", "US", "dwarf", "short,long"),
            ("Ragdoll", "US", "cobby", "long"),
        ],
    ),
    "shelters": pd.DataFrame(
        columns=("name", "city"),
        data=[
            ("01", "Paris"),
            ("02", "Chartres"),
            ("03", "Paris"),
        ],
    ),
}


class CatsDatabaseTarget(Target):
    """Toy 'Database' target for the local testing"""

    def __init__(self):
        super().__init__()
        self.args_names = {"view", "limit", "filter"}

    def __call__(
        self,
        view: str,
        limit: int = 3,
        filter: Optional[str] = None,
    ):
        """

        Parameters
        ----------
        view: Literal["cats", "breeds", "shelters"]
            "Table" to select data from
        limit: int
            Maximum number of results
        filter: str
            Filter expression that will be passed to DataFrame.query

        Returns
        -------
        Dataframe
        """
        result = DB[view].copy()
        if filter is not None:
            result.query(filter, inplace=True)
        return result[:limit]
