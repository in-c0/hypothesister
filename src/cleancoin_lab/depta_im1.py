import math

R_OUTER_NM = 0.15
R_CAVITY_GG_NM = 0.12


def event_probability(site_volume, domain_volume, available_count):
    if site_volume < 0 or domain_volume <= 0 or available_count < 0:
        raise ValueError("invalid inputs")
    return min(1.0, site_volume / domain_volume * available_count)


def hemisphere_volume(radius_nm):
    if radius_nm < 0:
        raise ValueError("invalid radius")
    return 2.0 * math.pi * radius_nm**3 / 3.0


def isolated_site_volume(interaction):
    if interaction == "GG-GG":
        return hemisphere_volume(R_OUTER_NM) + hemisphere_volume(R_CAVITY_GG_NM)
    if interaction == "MM-MM":
        return hemisphere_volume(R_OUTER_NM)
    if interaction == "XX":
        return 0.0
    raise ValueError("unknown interaction")
