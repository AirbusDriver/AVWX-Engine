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
