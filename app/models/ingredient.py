from . import db
from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, Integer, ForeignKey, Text, DateTime
import datetime

# Association table is defined in recipe.py; ensure import if needed
# (SQLAlchemy will use the same Table object across models)

class Ingredient(db.Model):
    __tablename__ = 'ingredient'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)

    # relationship back to Recipe via association table defined in recipe.py
    recipes = relationship('Recipe', secondary='recipe_ingredient', back_populates='ingredients')

    # ---------- CRUD methods ----------
    @staticmethod
    def create(session, name):
        ingredient = Ingredient(name=name)
        session.add(ingredient)
        session.commit()
        return ingredient

    @staticmethod
    def get_all(session):
        return session.query(Ingredient).all()

    @staticmethod
    def get_by_id(session, ingredient_id):
        return session.query(Ingredient).filter_by(id=ingredient_id).first()

    def update(self, session, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        session.commit()
        return self

    def delete(self, session):
        session.delete(self)
        session.commit()

    def __repr__(self):
        return f"<Ingredient {self.id} {self.name}>"
