ASSET_TYPES = [
    "POWER_PLANT",
    "SUBSTATION",
    "FACTORY",
    "RESIDENTIAL_AREA",
    "HOSPITAL",
    "DATA_CENTER",
    "SOLAR_FARM",
    "WIND_FARM",
    "BATTERY",
    "EV_CHARGER",
]

GENERATOR_TYPES = {"POWER_PLANT", "SOLAR_FARM", "WIND_FARM"}
CONSUMER_TYPES = {"FACTORY", "RESIDENTIAL_AREA", "HOSPITAL", "DATA_CENTER", "EV_CHARGER"}
STORAGE_TYPES = {"BATTERY"}

ASSET_STATUSES = ["NORMAL", "WARNING", "CRITICAL", "OVERLOAD"]

# Relative importance used by risk scoring / optimization in later parts.
# GridTwin_System_Design.md §26 — placeholder weights, not physically derived.
CRITICALITY_WEIGHTS = {
    "HOSPITAL": 1.00,
    "DATA_CENTER": 0.95,
    "FACTORY": 0.70,
    "RESIDENTIAL_AREA": 0.50,
    "EV_CHARGER": 0.40,
    "POWER_PLANT": 0.80,
    "SUBSTATION": 0.75,
    "SOLAR_FARM": 0.60,
    "WIND_FARM": 0.60,
    "BATTERY": 0.55,
}
