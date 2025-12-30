import random

from . import average_wedding_age
from .data_loader import dataset_load, _age_of_death

PERIODES = {
    "1891–1930": (1891, 1930),
    "1931–1960": (1931, 1960),
    "1961–1990": (1961, 1990),
    "1991–2016": (1991, 2016),
}
INFANT_TXT_MORTALITY = {
    "forte": "la mortalité infantile marquait encore fortement les familles",
    "moderee": "la mortalité infantile reculait progressivement",
    "faible": "la mortalité infantile était devenue rare",
}
NAMES_TXT = {
    "faible": "les prénoms se transmettaient souvent de génération en génération",
    "moyenne": "les prénoms commençaient à se diversifier",
    "elevee": "les prénoms étaient très variés",
}
DEATH_TXT = {
    "faible": "l’espérance de vie restait limitée",
    "moyenne": "l’espérance de vie progressait",
    "elevee": "l’espérance de vie était élevée",
}
WEDDING_TXT = {
    "precoce": "on se mariait généralement très jeune",
    "vingtaine": "le mariage avait souvent lieu dans la vingtaine",
    "tardif": "le mariage intervenait plutôt tard dans la vie",
}


death_df = dataset_load("liste_des_deces.csv")
wedding_df = dataset_load("liste_des_mariages.csv")
birth_df = dataset_load("liste_des_naissances.csv")


def filter_per_year(df, year_column, start, end):
    return df[(df[year_column] >= start) & (df[year_column] <= end)]


def stats_period(starting_date, end_date):
    stats = {}

    birth_period = filter_per_year(birth_df, "annee", starting_date, end_date)
    if not birth_period.empty:
        total = len(birth_period)
        top3 = birth_period["pr1"].value_counts().head(3).sum()
        stats["diversite_prenoms"] = top3 / total

    wedding_period = filter_per_year(wedding_df, "annee", starting_date, end_date)
    if not wedding_period.empty:
        avg = average_wedding_age(wedding_period)
        stats["age_mariage"] = (
            avg[["age_moyen_epoux", "age_moyen_epouse"]]
            .stack()
            .mean()
        )

    death_period = filter_per_year(death_df, "annee", starting_date, end_date)
    if not death_period.empty:
        death_ages = _age_of_death(death_period)["age_deces"]

        stats["age_deces"] = death_ages.mean()
        stats["mortalite_infantile"] = (death_ages < 1).mean()

    return stats

def wedding_category(age):
    if age < 25:
        return "precoce"
    elif age < 30:
        return "vingtaine"
    else:
        return "tardif"

def death_category(age):
    if age < 65:
        return "faible"
    elif age < 75:
        return "moyenne"
    else:
        return "elevee"

def first_name_ratio(top3_share):
    if top3_share > 0.4:
        return "faible"
    elif top3_share > 0.2:
        return "moyenne"
    else:
        return "elevee"

def infant_mortality(ratio):
    if ratio > 0.1:
        return "forte"
    elif ratio > 0.05:
        return "moderee"
    else:
        return "faible"



def generate_text(stats):
    phrases = []

    if "age_mariage" in stats:
        c = wedding_category(stats["age_mariage"])
        phrases.append(WEDDING_TXT[c])

    if "age_deces" in stats:
        c = death_category(stats["age_deces"])
        phrases.append(DEATH_TXT[c])

    if "diversite_prenoms" in stats:
        c = first_name_ratio(stats["diversite_prenoms"])
        phrases.append(NAMES_TXT[c])

    if "mortalite_infantile" in stats:
        c = infant_mortality(stats["mortalite_infantile"])
        phrases.append(INFANT_TXT_MORTALITY[c])

    random.shuffle(phrases)

    text = (
        "🏙️ *Imaginez....Rhodez, un.e habitant.e est né.e à une époque où*<br>"
        + ",<br>".join(f"*{p}*" for p in phrases[:3])
        + "."
    )
    return text
