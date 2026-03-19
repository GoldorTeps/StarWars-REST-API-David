from app import app
from models import db, People, Planets, Starships, User, Favorites

def seed_data():
    with app.app_context():
        # Clean current data to avoid duplicates if re-running
        db.drop_all()
        db.create_all()

        print("Seeding characters...")
        luke = People(
            name="Luke Skywalker", height=172, skin_color="fair", 
            hair_color="blond", eye_color="blue", birth_year="19BBY", 
            gender="male", home_world="Tatooine", 
            description="A legendary Jedi Master.", starships="X-wing"
        )
        leia = People(
            name="Leia Organa", height=150, skin_color="light", 
            hair_color="brown", eye_color="brown", birth_year="19BBY", 
            gender="female", home_world="Alderaan", 
            description="Princess of Alderaan.", starships="None"
        )
        
        print("Seeding planets...")
        tatooine = Planets(
            name="Tatooine", rotation_period=23, orbital_period=304, 
            diameter=10465, climate="arid", gravity="1 standard", 
            terrain="desert", population="200000"
        )
        
        print("Seeding starships...")
        xwing = Starships(
            name="X-wing", model="T-65 X-wing", manufacturer="Incom Corporation", 
            length=12, max_atmosphering_speed="1050", crew=1, 
            passengers=0, starship_class="Starfighter"
        )

        print("Seeding users...")
        vader = User(email="dvader@empire.com", password="darkside_user_1", is_active=True)
        
        db.session.add_all([luke, leia, tatooine, xwing, vader])
        db.session.commit()

        print("Seeding favorites for Vader...")
        favs = Favorites(user_id=vader.id)
        favs.people.append(luke)
        favs.planets.append(tatooine)
        favs.starships.append(xwing)
        
        db.session.add(favs)
        db.session.commit()
        
        print("Galaxy populated successfully!")

if __name__ == "__main__":
    seed_data()
