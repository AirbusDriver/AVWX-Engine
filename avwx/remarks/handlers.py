from avwx.parsing import AtomHandler

from . import atoms
from . import translations as trans

# todo: simple translations should have their own class method
aircraft_mishap_handler = AtomHandler(
    atoms.aircraft_mishap_atom, lambda a, s: "Aircraft mishap"
)

begin_end_precip_handler = AtomHandler(
    atoms.begin_end_precip_and_ts_atom, trans.begin_end_of_precip_trans
)

ceiling_height_at_second_location_handler = AtomHandler(
    atoms.ceiling_height_at_second_location_atom,
    trans.ceiling_height_at_second_location_trans,
)
