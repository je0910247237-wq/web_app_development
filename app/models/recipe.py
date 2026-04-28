from . import db
from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, Integer, ForeignKey, Text, DateTime
import datetime

# Association table for many-to-many relationship
recipe_ingredient = Table(
    'recipe_ingredient',
    db.metadata,
    Column('recipe_id', Integer, ForeignKey('recipe.id', ondelete='CASCADE'), primary_key=True),
    Column('ingredient_id', Integer, ForeignKey('ingredient.id', ondelete='CASCADE'), primary_key=True)
)

class Recipe(db.Model):
    __tablename__ = 'recipe'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(Text, nullable=False)
    description = Column(Text)
    steps = Column(Text)  # could store JSON or newline separated steps
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # relationship to Ingredient via association table
    ingredients = relationship('Ingredient', secondary=recipe_ingredient, back_populates='recipes')

    # ---------- CRUD methods ----------
    @staticmethod
    def create(session, title, description=None, steps=None, ingredient_ids=None):
        """Create a new recipe and associate ingredients.
        `ingredient_ids` should be an iterable of existing Ingredient ids.
        """
        recipe = Recipe(title=title, description=description, steps=steps)
        if ingredient_ids:
            ingredients = session.query(Ingredient).filter(Ingredient.id.in_(ingredient_ids)).all()
            recipe.ingredients = ingredients
        session.add(recipe)
        session.commit()
        return recipe

    @staticmethod
    def get_all(session):
        return session.query(Recipe).all()

    @staticmethod
    def get_by_id(session, recipe_id):
        return session.query(Recipe).filter_by(id=recipe_id).first()

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
        return f"<Recipe {self.id} {self.title}>"
