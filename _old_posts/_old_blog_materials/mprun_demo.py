
def converter(heroes, heights, weights):
    new_hts = heights * 0.39370
    new_wts = weights * 2.20462

    hero_data = {}

    for i, hero in enumerate(heroes):
        hero_data[hero] = (new_hts[i], new_wts[i])

    return hero_data
