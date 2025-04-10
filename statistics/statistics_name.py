from collections import Counter
from bs4 import BeautifulSoup

def make_stat():
    stat = {}
    with open("home.html", encoding="cp1251") as file:
        html = file.read()
    soup = BeautifulSoup(html, "html.parser")

    current_year = None
    for tr in soup.find_all("tr"):
        h3 = tr.find("h3")
        if h3:
            current_year = h3.get_text().strip()
            stat[current_year] = {"male": Counter(), "female": Counter()}
        else:
            a = tr.find("a")
            if a and current_year is not None:
                full_name = a.get_text().strip()
                name = full_name.split()[1] if len(full_name.split()) >= 2 else full_name.split()[0]
                if name.lower() in ["илья", "никита", "лёва", "игорь"]:
                    gender = "male"
                elif name[-1].lower() in ["а", "я", "ь"]:
                    gender = "female"
                else:
                    gender = "male"
                stat[current_year][gender][name] += 1
    return stat

def extract_years(stat):
    return sorted(stat.keys(), key=lambda x: int(x))

def extract_general(stat):
    total = Counter()
    for year in stat:
        total += stat[year]["male"]
        total += stat[year]["female"]
    return sorted(total.items(), key=lambda item: item[1], reverse=True)

def extract_general_male(stat):
    total = Counter()
    for year in stat:
        total += stat[year]["male"]
    return sorted(total.items(), key=lambda item: item[1], reverse=True)

def extract_general_female(stat):
    total = Counter()
    for year in stat:
        total += stat[year]["female"]
    return sorted(total.items(), key=lambda item: item[1], reverse=True)

def extract_year(stat, year):
    if year not in stat:
        return []
    return sorted((stat[year]["male"] + stat[year]["female"]).items(), key=lambda item: item[1], reverse=True)

def extract_year_male(stat, year):
    if year not in stat:
        return []
    return sorted(stat[year]["male"].items(), key=lambda item: item[1], reverse=True)


def extract_year_female(stat, year):
    if year not in stat:
        return []
    return sorted(stat[year]["female"].items(), key=lambda item: item[1], reverse=True)

print("Years:", extract_years(make_stat()))
print("Year:", extract_year(make_stat(), 2011))
print("General:", extract_general(make_stat()))
print("General male:", extract_general_male(make_stat()))
print("General year male:", extract_year_male(make_stat(), 2010))
print("General female:", extract_general_female(make_stat()))
print("General year female:", extract_year_female(make_stat(), 2009))
