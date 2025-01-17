from sqlalchemy import create_engine, Column, Integer, Text, TIMESTAMP, text, MetaData, ForeignKey, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import os
from dotenv import load_dotenv
import pymysql
from datetime import datetime

# Charger les variables d'environnement
load_dotenv()

# Configuration de la base de données
DATABASE_URL = os.getenv('DATABASE_URL')
print(f"Tentative de connexion à : {DATABASE_URL}")

# Créer la base de données si elle n'existe pas
def create_database():
    try:
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password=''
        )
        with connection.cursor() as cursor:
            cursor.execute("DROP DATABASE IF EXISTS spam")
            cursor.execute("CREATE DATABASE spam")
            cursor.execute("USE spam")
            
            # Créer la table users
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(255) NOT NULL,
                    email VARCHAR(255) NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Créer la table messages
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    message TEXT NOT NULL,
                    result VARCHAR(50) NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            """)
            
            # Créer la table mots_spam
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS mots_spam (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    word VARCHAR(255) NOT NULL
                )
            """)
            
            print("Base de données et tables créées avec succès")
            
            # Insérer des utilisateurs de test
            cursor.execute("SELECT COUNT(*) FROM users")
            if cursor.fetchone()[0] == 0:
                cursor.execute("""
                    INSERT INTO users (username, email, password) VALUES 
                    ('alice', 'alice@test.com', 'password123'),
                    ('bob', 'bob@test.com', 'password456'),
                    ('charlie', 'charlie@test.com', 'password789')
                """)
                
                # Insérer quelques messages de test
                cursor.execute("""
                    INSERT INTO messages (user_id, message, result) VALUES 
                    (1, 'Hello world', 'not_spam'),
                    (1, 'Buy now!', 'spam'),
                    (2, 'Meeting tomorrow', 'not_spam')
                """)
                
                # Insérer des mots spam de test si la table est vide
                cursor.execute("SELECT COUNT(*) FROM mots_spam")
                if cursor.fetchone()[0] == 0:
                    cursor.execute("""
                        INSERT INTO mots_spam (word) VALUES 
                        ('spam'),
                        ('buy'),
                        ('free'),
                        ('win'),
                        ('viagra')
                    """)
                
                connection.commit()
                print("Données de test insérées")
            
    except Exception as e:
        print(f"Erreur MySQL: {e}")
    finally:
        connection.close()

# Créer la base de données et la table
create_database()

# Création de l'engine
engine = create_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True,
    pool_recycle=3600
)

# Créer la session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Créer la base
metadata = MetaData()
Base = declarative_base(metadata=metadata)

# Modèle User
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))

    # Relation avec Message
    messages = relationship("Message", back_populates="user")

    def __str__(self):
        return f"User(id={self.id}, username={self.username})"

# Modèle Message
class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    message = Column(String(1000), nullable=False)
    result = Column(String(50), nullable=False)
    timestamp = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))

    # Relation avec User
    user = relationship("User", back_populates="messages")

# Modèle MotSpam
class MotSpam(Base):
    __tablename__ = "mots_spam"

    id = Column(Integer, primary_key=True, autoincrement=True)
    word = Column(String(255), nullable=False)

    def __str__(self):
        return f"MotSpam(word='{self.word}')"

# Fonction pour obtenir la session DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# S'assurer que les tables sont créées
metadata.create_all(bind=engine)