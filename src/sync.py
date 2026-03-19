import requests
from app import app
from models import db, People, Planets, Starships, User

def fetch_all(endpoint):
    results = []
    url = f"https://swapi.dev/api/{endpoint}/"
    while url:
        print(f"Fetching {endpoint} from {url}...")
        resp = requests.get(url).json()
        results.extend(resp["results"])
        url = resp.get("next")
    return results

def sync_swapi():
    with app.app_context():
        print("Cleaning the galaxy (excluding users)...")
        People.query.delete()
        Planets.query.delete()
        Starships.query.delete()
        db.session.commit()

        # Sync Characters
        print("Syncing characters...")
        all_people = fetch_all("people")
        for item in all_people:
            sw_id = item["url"].split("/")[-2]
            person = People(
                name=item["name"],
                height=int(item["height"]) if item["height"].isdigit() else 0,
                skin_color=item["skin_color"],
                hair_color=item["hair_color"],
                eye_color=item["eye_color"],
                birth_year=item["birth_year"],
                gender=item["gender"],
                home_world=item["homeworld"],
                description="A character from the Star Wars universe.",
                starships=", ".join(item["starships"][:1]),
                image_url=f"https://raw.githubusercontent.com/sippinwindex/star-wars-guide-Fork/master/build/assets/img/characters/{sw_id}.jpg"
            )
            db.session.add(person)
        
        # Sync Planets
        print("Syncing planets...")
        all_planets = fetch_all("planets")
        for item in all_planets:
            sw_id = item["url"].split("/")[-2]
            planet = Planets(
                name=item["name"],
                rotation_period=int(item["rotation_period"]) if item["rotation_period"].isdigit() else 0,
                orbital_period=int(item["orbital_period"]) if item["orbital_period"].isdigit() else 0,
                diameter=int(item["diameter"]) if item["diameter"].isdigit() else 0,
                climate=item["climate"],
                gravity=item["gravity"],
                terrain=item["terrain"],
                population=item["population"],
                image_url=f"https://raw.githubusercontent.com/sippinwindex/star-wars-guide-Fork/master/build/assets/img/planets/{sw_id}.jpg"
            )
            db.session.add(planet)

        # Sync Starships
        print("Syncing starships...")
        all_starships = fetch_all("starships")
        for item in all_starships:
            sw_id = item["url"].split("/")[-2]
            ship = Starships(
                name=item["name"],
                model=item["model"],
                manufacturer=item["manufacturer"],
                length=int(float(item["length"].replace(",", ""))) if item["length"].replace(",", "").replace(".", "").isdigit() else 0,
                max_atmosphering_speed=item["max_atmosphering_speed"],
                crew=int(item["crew"].replace(",", "")) if item["crew"].replace(",", "").isdigit() else 0,
                passengers=int(item["passengers"].replace(",", "")) if item["passengers"].replace(",", "").isdigit() else 0,
                starship_class=item["starship_class"],
                image_url=f"https://raw.githubusercontent.com/sippinwindex/star-wars-guide-Fork/master/build/assets/img/starships/{sw_id}.jpg"
            )
            db.session.add(ship)

        db.session.commit()
        print("Galaxy fully synchronized with SWAPI!")

if __name__ == "__main__":
    sync_swapi()
