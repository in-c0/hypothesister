def event_probability(site_volume, domain_volume, available_count):
    if site_volume < 0 or domain_volume <= 0 or available_count < 0:
        raise ValueError("invalid inputs")
    return min(1.0, site_volume / domain_volume * available_count)
