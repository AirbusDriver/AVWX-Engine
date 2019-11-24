from avwx.parsing import RegexAtom

from . import patterns as ptn


aircraft_mishap_atom = RegexAtom(ptn.AIRCRAFT_MISHAP_RE, "Aircraft Mishap")

automated_station_atom = RegexAtom(ptn.AUTOMATED_STATION_RE, "Automated Station")

begin_end_precip_and_ts_atom = RegexAtom(
    ptn.BEGINNING_ENDING_OF_PRECIP_AND_TS, "Begin/End Precip/TS"
)

ceiling_height_at_second_location_atom = RegexAtom(
    ptn.CEILING_HEIGHT_AT_SECOND_LOCATION_RE, "Ceiling Height at Second Location"
)

lightning_atom = RegexAtom(ptn.LIGHTNING_RE, "Lightning Activity")

peak_wind_atom = RegexAtom(ptn.PEAK_WIND_RE, "Peak Wind")

pressure_change_atom = RegexAtom(ptn.PRESSURE_CHANGE_RE, "Pressure Change")

remarks_identifier_atom = RegexAtom(ptn.REMARKS_IDENTIFIER_RE, "Remarks Identifier")

sea_level_pressure_atom = RegexAtom(ptn.SEA_LEVEL_PRESSURE_RE, "Sea Level Pressure")

tornado_activity_atom = RegexAtom(ptn.TORNADO_ACTIVITY_RE, "Tornado Activity")

tower_or_surface_visibilty_atom = RegexAtom(
    ptn.TOWER_OR_SURFACE_VISIBILITY_RE, "Tower or Surface Visbility"
)


variable_ceiling_height_atom = RegexAtom(
    ptn.VARIABLE_CEILING_HEIGHT_RE, "Variable Ceiling Height"
)

virga_atom = RegexAtom(ptn.VIRGA_RE, "Virga")

visibility_at_second_location_atom = RegexAtom(
    ptn.VISIBILITY_AT_SECOND_LOCATION_RE, "Visibility at Second Location"
)

wind_shift_atom = RegexAtom(ptn.WIND_SHIFT_RE, "Wind Shift")
