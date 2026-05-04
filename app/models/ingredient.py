from app import get_db_connection

class Ingredient:
    @staticmethod
    def get_all():
        conn = get_db_connection()
        try:
            ingredients = conn.execute('SELECT * FROM ingredient ORDER BY name').fetchall()
            return ingredients
        except Exception as e:
            print(f"Error getting ingredients: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def create(name):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO ingredient (name) VALUES (?)', (name,))
            ingredient_id = cursor.lastrowid
            conn.commit()
            return ingredient_id
        except Exception as e:
            print(f"Error creating ingredient: {e}")
            conn.rollback()
            return None
        finally:
            conn.close()

    @staticmethod
    def delete(ingredient_id):
        conn = get_db_connection()
        try:
            conn.execute('DELETE FROM ingredient WHERE id = ?', (ingredient_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting ingredient: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()
