from app import get_db_connection
from datetime import datetime

class Recipe:
    @staticmethod
    def get_all(search_query=None):
        conn = get_db_connection()
        try:
            if search_query:
                recipes = conn.execute(
                    'SELECT * FROM recipe WHERE title LIKE ? ORDER BY created_at DESC',
                    ('%' + search_query + '%',)
                ).fetchall()
            else:
                recipes = conn.execute('SELECT * FROM recipe ORDER BY created_at DESC').fetchall()
            return recipes
        except Exception as e:
            print(f"Error getting recipes: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def get_by_id(recipe_id):
        conn = get_db_connection()
        try:
            recipe = conn.execute('SELECT * FROM recipe WHERE id = ?', (recipe_id,)).fetchone()
            if not recipe:
                return None
            
            ingredients = conn.execute('''
                SELECT i.id, i.name 
                FROM ingredient i
                JOIN recipe_ingredient ri ON i.id = ri.ingredient_id
                WHERE ri.recipe_id = ?
            ''', (recipe_id,)).fetchall()
            
            recipe_dict = dict(recipe)
            recipe_dict['ingredients'] = ingredients
            return recipe_dict
        except Exception as e:
            print(f"Error getting recipe: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def create(title, description, steps, ingredient_ids):
        conn = get_db_connection()
        try:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO recipe (title, description, steps, created_at, updated_at) VALUES (?, ?, ?, ?, ?)',
                (title, description, steps, now, now)
            )
            recipe_id = cursor.lastrowid
            
            for i_id in ingredient_ids:
                cursor.execute(
                    'INSERT INTO recipe_ingredient (recipe_id, ingredient_id) VALUES (?, ?)',
                    (recipe_id, i_id)
                )
            conn.commit()
            return recipe_id
        except Exception as e:
            print(f"Error creating recipe: {e}")
            conn.rollback()
            return None
        finally:
            conn.close()

    @staticmethod
    def update(recipe_id, title, description, steps, ingredient_ids):
        conn = get_db_connection()
        try:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor = conn.cursor()
            cursor.execute(
                'UPDATE recipe SET title = ?, description = ?, steps = ?, updated_at = ? WHERE id = ?',
                (title, description, steps, now, recipe_id)
            )
            
            cursor.execute('DELETE FROM recipe_ingredient WHERE recipe_id = ?', (recipe_id,))
            for i_id in ingredient_ids:
                cursor.execute(
                    'INSERT INTO recipe_ingredient (recipe_id, ingredient_id) VALUES (?, ?)',
                    (recipe_id, i_id)
                )
            conn.commit()
            return True
        except Exception as e:
            print(f"Error updating recipe: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()

    @staticmethod
    def delete(recipe_id):
        conn = get_db_connection()
        try:
            conn.execute('DELETE FROM recipe WHERE id = ?', (recipe_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting recipe: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()
