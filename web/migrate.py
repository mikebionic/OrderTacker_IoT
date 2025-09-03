#!/usr/bin/env python3

from dotenv import load_dotenv

load_dotenv()

from main import create_app, db
from main.config import Config
from main.models import User, Finger, Location

def migrate_database():
    """Initialize and populate the database with sample data."""
    
    app = create_app()

    with app.app_context():
        try:
            print("Starting database migration...")
            
            print("Dropping existing tables...")
            db.drop_all()
            
            print("Creating new tables...")
            db.create_all()

            print(f"Creating admin user: {Config.ADMIN_USERNAME}")
            admin_user = User(username=Config.ADMIN_USERNAME, pin=Config.ADMIN_PIN)
            db.session.add(admin_user)

            users_data = [
                {
                    "id": 2,
                    "username": "plan",
                    "name": "Plan",
                    "surname": "Planyyew",
                    "patronomic": "Planyyewic",
                    "position": "Iş ýörediji",
                    "pin": "",
                    "avatar": "",
                },
                {
                    "id": 3,
                    "username": "jemal",
                    "name": "Jemal",
                    "surname": "Planyyewa",
                    "patronomic": "Planyyewna",
                    "position": "Mugallym",
                    "pin": "",
                    "avatar": "",
                }
            ]

            fingerprint_tags = [
                {
                    "id": 1,
                    "user_id": 2,
                    "code": "8B:44:12:22",
                    "name": "Plan's Card",
                },
                {
                    "id": 2,
                    "user_id": 3,
                    "code": "84:33:2:12:22",
                    "name": "Jemal's Card",
                }
            ]

            locations_data = [
                {
                    "id": 1,
                    "name": "study_place",
                    "full_name": "Plan yerin plan bolumcesenin okuw binasy",
                    "address": "Parahat 01",
                    "latitude": "11112",
                    "longitude": "92323",
                },
                {
                    "id": 2,
                    "name": "entrance",
                    "full_name": "Plan yerin girelgesi",
                    "address": "Parahat 01",
                    "latitude": "11121",
                    "longitude": "92333",
                },
            ]

            print(f"Adding {len(users_data)} users...")
            for user_data in users_data:
                current_user = User(**user_data)
                db.session.add(current_user)

            print(f"Adding {len(fingerprint_tags)} fingerprint tags...")
            for finger_data in fingerprint_tags:
                current_finger = Finger(**finger_data)
                db.session.add(current_finger)

            print(f"Adding {len(locations_data)} locations...")
            for location_data in locations_data:
                current_location = Location(**location_data)
                db.session.add(current_location)

            print("Committing changes to database...")
            db.session.commit()
            
            print("\n" + "="*50)
            print("✅ Database migration completed successfully!")
            print("="*50)
            print(f"📋 Summary:")
            print(f"   • Admin user: {Config.ADMIN_USERNAME}")
            print(f"   • Regular users: {len(users_data)}")
            print(f"   • RFID cards: {len(fingerprint_tags)}")
            print(f"   • Locations: {len(locations_data)}")
            print("="*50)
            
        except Exception as e:
            print(f"❌ Error during migration: {str(e)}")
            db.session.rollback()
            raise
        finally:
            db.session.close()

if __name__ == "__main__":
    migrate_database()