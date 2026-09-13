
from enum import StrEnum, auto


class MotionThemeEnum(StrEnum):
    unknown = auto()
    international_relationship = auto()
    economics = auto()
    politics = auto()
    science_medicine = auto()
    AI_technologies = auto()
    philosophy_religion = auto()
    law_crime = auto()
    education = auto()
    art = auto()
    feminism = auto()
    sport = auto()
    conflict = auto()
    urbanism = auto()
    media = auto()
    LGBTQ = auto()
    europe = auto()
    asia = auto()
    central_asia = auto()
    kazakhstan = auto()
    social = auto()
    prefers_world = auto()
    
class MotionTypeEnum(StrEnum):
    unknown = auto()
    this_house_believes_that = auto()
    this_house_opposes = auto()
    this_house_prefer = auto()
    this_house_regrets = auto()
    this_house_supports = auto()
    this_house_would = auto()
    