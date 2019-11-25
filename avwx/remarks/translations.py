from avwx.parsing import BaseAtom, TranslationError


def begin_end_of_precip_trans(atom: BaseAtom, string: str) -> str:
    """Rain|Thunderstorm began|ended at [HH]MM [and ended at [HH]MM]"""
    match = atom.to_atom_span(string).match

    if match:
        data = atom.to_data_dict(match)
    else:
        raise TranslationError(f"no match could be made from {string}")

    precip_options = {"RA": "Rain", "TS": "Thunderstorm"}

    time_options = {"B": "began", "E": "ended"}

    precip = precip_options.get(data["precip"])
    first_time_type = time_options.get(data["first_type"])
    first_time = data.get("first_time")

    first_string = f"{first_time_type} at {first_time}"

    out = f"{precip} {first_string}"

    if data.get("second"):
        second_time_type = time_options.get(data["second_type"])
        second_time = data.get("second_time")

        second_string = f"and {second_time_type} at {second_time}"

        out = f"{out} {second_string}"

    return out


def ceiling_height_at_second_location_trans(atom: BaseAtom, string: str) -> str:
    """Ceiling height DDD over runway DD[LCR]"""
    match = atom.to_atom_span(string).match

    if match:
        data = atom.to_data_dict(match)
    else:  # todo: make decorator
        raise TranslationError(f"no match could be made from {string}")

    height = data["height"]
    runway = data["location"]
    runway_nums = "".join(char for char in runway if char.isdigit())

    suffix = {"L": " left", "C": " center", "R": " right"}.get(runway[-1], "")

    runway_string = f"{runway_nums}{suffix}"

    out = f"Ceiling height {height} over runway {runway_string}"
    return out
