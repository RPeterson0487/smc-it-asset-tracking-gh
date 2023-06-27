"""Database manager configuration for IT Asset Tracking"""

old_tables = (
    "IT_Assets_DT",
    "IT_Assets_FT",
    "IT_Assets_LT",
    "IT_Assets_PR",
    "IT_Assets_SG",
    "IT_Assets_SV",
    "IT_Assets_SW",
    "IT_Assets_TB",
    "IT_Assets_TC",
)

new_tables = (
    "IT_Assets",
)

search_tables = old_tables + new_tables

insert_table = "IT_Assets"

test_serials = (
    "aa002"
)