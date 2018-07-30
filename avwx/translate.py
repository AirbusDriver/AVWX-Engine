"""
Contains functions for translating report data
"""

from avwx import core, remarks
from avwx.static import CLOUD_TRANSLATIONS, WX_TRANSLATIONS, \
                        TURBULANCE_CONDITIONS, ICING_CONDITIONS
from avwx.structs import MetarData, MetarTrans, ReportData, TafData, TafLineTrans, TafTrans, Units


def get_cardinal_direction(wdir: int) -> str:
    """
    Returns the cardinal direction (NSEW) for a degree direction

    Wind Direction - Cheat Sheet:

    (360) -- 011/012 -- 033/034 -- (045) -- 056/057 -- 078/079 -- (090)

    (090) -- 101/102 -- 123/124 -- (135) -- 146/147 -- 168/169 -- (180)

    (180) -- 191/192 -- 213/214 -- (225) -- 236/237 -- 258/259 -- (270)

    (270) -- 281/282 -- 303/304 -- (315) -- 326/327 -- 348/349 -- (360)
    """
    ret = ''
    if not isinstance(wdir, int):
        wdir = int(wdir)
    # Convert to range [0 360]
    while wdir < 0:
        wdir += 360
    wdir = wdir % 360
    if 304 <= wdir <= 360 or 0 <= wdir <= 56:
        ret += 'N'
        if 304 <= wdir <= 348:
            if 327 <= wdir <= 348:
                ret += 'N'
            ret += 'W'
        elif 12 <= wdir <= 56:
            if 12 <= wdir <= 33:
                ret += 'N'
            ret += 'E'
    elif 124 <= wdir <= 236:
        ret += 'S'
        if 124 <= wdir <= 168:
            if 147 <= wdir <= 168:
                ret += 'S'
            ret += 'E'
        elif 192 <= wdir <= 236:
            if 192 <= wdir <= 213:
                ret += 'S'
            ret += 'W'
    elif 57 <= wdir <= 123:
        ret += 'E'
        if 57 <= wdir <= 78:
            ret += 'NE'
        elif 102 <= wdir <= 123:
            ret += 'SE'
    elif 237 <= wdir <= 303:
        ret += 'W'
        if 237 <= wdir <= 258:
            ret += 'SW'
        elif 282 <= wdir <= 303:
            ret += 'NW'
    return ret


def wind(wdir: str, wspd: str, wgst: str, wvar: [str] = None, unit: str = 'kt', cardinals: bool = True) -> str:
    """
    Format wind elements into a readable sentence

    Returns the translation string

    Ex: NNE-020 (variable 010 to 040) at 14kt gusting to 20kt
    """
    ret = ''
    if wdir == '000':
        ret += 'Calm'
    elif wdir.isdigit():
        if cardinals:
            ret += get_cardinal_direction(wdir) + '-'
        ret += wdir
    elif wdir == 'VRB':
        ret += 'Variable'
    else:
        ret += wdir
    if wvar and isinstance(wvar, list):
        ret += f' (variable {wvar[0]} to {wvar[1]})'
    if wspd and wspd not in ('0', '00'):
        ret += f' at {wspd}{unit}'
    if wgst:
        ret += f' gusting to {wgst}{unit}'
    return ret


def visibility(vis: str, unit: str = 'm') -> str:
    """
    Formats a visibility element into a string with both km and sm values

    Ex: 8km ( 5sm )
    """
    if vis == 'P6':
        return 'Greater than 6sm ( >10km )'
    if vis == 'M1/4':
        return 'Less than .25sm ( <0.4km )'
    if '/' in vis and not core.is_unknown(vis):
        vis = float(vis[:vis.find('/')]) / int(vis[vis.find('/') + 1:])
    try:
        float(vis)
    except ValueError:
        return ''
    if unit == 'm':
        converted = float(vis) * 0.000621371
        converted = str(round(converted, 1)).replace('.0', '') + 'sm'
        vis = str(round(int(vis) / 1000, 1)).replace('.0', '')
        unit = 'km'
    elif unit == 'sm':
        converted = float(vis) / 0.621371
        converted = str(round(converted, 1)).replace('.0', '') + 'km'
        vis = str(vis).replace('.0', '')
    else:
        return ''
    return f'{vis}{unit} ({converted})'


def temperature(temp: str, unit: str = 'C') -> str:
    """
    Formats a temperature element into a string with both C and F values

    Used for both Temp and Dew

    Ex: 34°C (93°F)
    """
    temp = temp.replace('M', '-')
    try:
        temp = int(temp)
    except ValueError:
        return ''
    unit = unit.upper()
    if unit == 'C':
        converted = int(temp) * 1.8 + 32
        converted = str(int(round(converted))) + '°F'
    elif unit == 'F':
        converted = (int(temp) - 32) / 1.8
        converted = str(int(round(converted))) + '°C'
    else:
        return ''
    return f'{temp}°{unit} ({converted})'


def altimeter(alt: str, unit: str = 'hPa') -> str:
    """
    Formats the altimter element into a string with hPa and inHg values

    Ex: 30.11 inHg (10.20 hPa)
    """
    if not alt.isdigit():
        if len(alt) == 5 and alt[1:].isdigit():
            alt = alt[1:]
        else:
            return ''
    if unit == 'hPa':
        converted = float(alt) / 33.8638866667
        converted = str(round(converted, 2)) + ' inHg'
    elif unit == 'inHg':
        alt = alt[:2] + '.' + alt[2:]
        converted = float(alt) * 33.8638866667
        converted = str(int(round(converted))) + ' hPa'
    else:
        return ''
    return f'{alt} {unit} ({converted})'


def clouds(clds: [str], unit: str = 'ft') -> str:
    """
    Format cloud list into a readable sentence

    Returns the translation string

    Ex: Broken layer at 2200ft (Cumulonimbus), Overcast layer at 3600ft - Reported AGL
    """
    ret = []
    for cloud in clds:
        if len(cloud) == 2 and cloud[1].isdigit() and cloud[0] in CLOUD_TRANSLATIONS:
            ret.append(CLOUD_TRANSLATIONS[cloud[0]].format(int(cloud[1]) * 100, unit))
        elif len(cloud) == 3 and cloud[1].isdigit() \
            and cloud[0] in CLOUD_TRANSLATIONS and cloud[2] in CLOUD_TRANSLATIONS:
            cloudstr = CLOUD_TRANSLATIONS[cloud[0]] + ' (' + CLOUD_TRANSLATIONS[cloud[2]] + ')'
            ret.append(cloudstr.format(int(cloud[1]) * 100, unit))
    if ret:
        return ', '.join(ret) + ' - Reported AGL'
    return 'Sky clear'


def wxcode(code: str) -> str:
    """
    Translates weather codes into readable strings

    Returns translated string of variable length
    """
    if not code:
        return ''
    ret = ''
    if code[0] == '+':
        ret = 'Heavy '
        code = code[1:]
    elif code[0] == '-':
        ret = 'Light '
        code = code[1:]
    #Return code if code is not a code, ex R03/03002V03
    if len(code) not in [2, 4, 6]:
        return code
    for _ in range(len(code) // 2):
        if code[:2] in WX_TRANSLATIONS:
            ret += WX_TRANSLATIONS[code[:2]] + ' '
        else:
            ret += code[:2]
        code = code[2:]
    return ret.strip(' ')


def other_list(wxcodes: [str]) -> str:
    """
    Translate the list of wx codes (otherList) into a readable sentence

    Returns the translation string
    """
    return ', '.join([wxcode(code) for code in wxcodes])


def wind_shear(shear: str, unit_alt: str = 'ft', unit_wnd: str = 'kt') -> str:
    """
    Translate wind shear into a readable string

    Ex: Wind shear 2000ft from 140 at 30kt
    """
    if not shear or 'WS' not in shear or '/' not in shear:
        return ''
    shear = shear[2:].rstrip(unit_wnd.upper()).split('/')
    return 'Wind shear {alt}{unit_alt} from {winddir} at {speed}{unit_wind}'.format(
        alt=int(shear[0]) * 100, unit_alt=unit_alt, winddir=shear[1][:3],
        speed=shear[1][3:], unit_wind=unit_wnd)


def turb_ice(turbice: [str], unit: str = 'ft') -> str:
    """
    Translate the list of turbulance or icing into a readable sentence

    Ex: Occasional moderate turbulence in clouds from 3000ft to 14000ft
    """
    if not turbice:
        return ''
    #Determine turbulance or icing
    if turbice[0][0] == '5':
        conditions = TURBULANCE_CONDITIONS
    elif turbice[0][0] == '6':
        conditions = ICING_CONDITIONS
    else:
        return ''
    #Create list of split items (type, floor, height)
    split = []
    for item in turbice:
        if len(item) == 6:
            split.append([item[1:2], item[2:5], item[5]])
    #Combine items that cover a layer greater than 9000ft
    for i in reversed(range(len(split) - 1)):
        if split[i][2] == '9' and split[i][0] == split[i + 1][0] \
            and int(split[i + 1][1]) == (int(split[i][1]) + int(split[i][2]) * 10):
            split[i][2] = str(int(split[i][2]) + int(split[i + 1][2]))
            split.pop(i + 1)
    #Return joined, formatted string from split items
    return ', '.join(['{conditions} from {low_alt}{unit} to {high_alt}{unit}'.format(
        conditions=conditions[item[0]], low_alt=int(item[1]) * 100,
        high_alt=int(item[1]) * 100 + int(item[2]) * 1000, unit=unit) for item in split])


def min_max_temp(temp: str, unit: str = 'C') -> str:
    """
    Format the Min and Max temp elemets into a readable string

    Ex: Maximum temperature of 23°C (73°F) at 18-15:00Z
    """
    if not temp or len(temp) < 7:
        return ''
    if temp[:2] == 'TX':
        temp_type = 'Maximum'
    elif temp[:2] == 'TN':
        temp_type = 'Minimum'
    else:
        return ''
    temp = temp[2:].replace('M', '-').replace('Z', '').split('/')
    if len(temp[1]) > 2:
        temp[1] = temp[1][:2] + '-' + temp[1][2:]
    return f'{temp_type} temperature of {temperature(temp[0], unit)} at {temp[1]}:00Z'


def shared(wxdata: ReportData, units: Units) -> {str: str}:
    """
    Translate Visibility, Altimeter, Clouds, and Other
    """
    translations = {}
    translations['visibility'] = visibility(wxdata.visibility, units.visibility)
    translations['altimeter'] = altimeter(wxdata.altimeter, units.altimeter)
    translations['clouds'] = clouds(wxdata.clouds, units.altitude)
    translations['other'] = other_list(wxdata.other)
    return translations


def metar(wxdata: MetarData, units: Units) -> MetarTrans:
    """
    Translate the results of metar.parse

    Keys: Wind, Visibility, Clouds, Temperature, Dewpoint, Altimeter, Other
    """
    translations = shared(wxdata, units)
    translations['wind'] = wind(wxdata.wind_direction, wxdata.wind_speed,
                                wxdata.wind_gust, wxdata.wind_variable_direction,
                                units.wind_speed)
    translations['temperature'] = temperature(wxdata.temperature, units.temperature)
    translations['dewpoint'] = temperature(wxdata.dewpoint, units.temperature)
    translations['remarks'] = remarks.translate(wxdata.remarks)
    return MetarTrans(**translations)


def taf(wxdata: TafData, units: Units) -> TafTrans:
    """
    Translate the results of taf.parse

    Keys: Forecast, Min-Temp, Max-Temp

    Forecast keys: Wind, Visibility, Clouds, Altimeter, Wind-Shear, Turbulance, Icing, Other
    """
    translations = {'forecast': []}
    for line in wxdata.forecast:
        trans = shared(line, units)
        trans['wind'] = wind(line.wind_direction, line.wind_speed,
                             line.wind_gust, unit=units.wind_speed)
        trans['wind_shear'] = wind_shear(line.wind_shear, units.altitude, units.wind_speed)
        trans['turbulance'] = turb_ice(line.turbulance, units.altitude)
        trans['icing'] = turb_ice(line.icing, units.altitude)
        # Remove false 'Sky Clear' if line type is 'BECMG'
        if line.type == 'BECMG' and trans['clouds'] == 'Sky clear':
            trans['clouds'] = None
        translations['forecast'].append(TafLineTrans(**trans))
    translations['min_temp'] = min_max_temp(wxdata.min_temp, units.temperature)
    translations['max_temp'] = min_max_temp(wxdata.max_temp, units.temperature)
    translations['remarks'] = remarks.translate(wxdata.remarks)
    return TafTrans(**translations)
