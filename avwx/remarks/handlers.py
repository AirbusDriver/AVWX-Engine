from avwx.parsing import AtomHandler

from . import atoms
from . import translations as trans


automated_station_handler = AtomHandler(atoms.automated_station_atom)

aircraft_mishap_handler = AtomHandler(
    atoms.aircraft_mishap_atom, lambda a, s: "Aircraft mishap"
)

begin_end_precip_handler = AtomHandler(
    atoms.begin_end_precip_and_ts_atom, trans.begin_end_of_precip_trans
)
