from flask import Blueprint, request, render_template, redirect, url_for, flash
from app.models.ingredient import Ingredient

ingredient_bp = Blueprint('ingredient', __name__)

@ingredient_bp.route('/ingredients', methods=['GET'])
def list_ingredients():
    ingredients = Ingredient.get_all()
    return render_template('ingredients/index.html', ingredients=ingredients)

@ingredient_bp.route('/ingredients/create', methods=['POST'])
def create_ingredient():
    name = request.form.get('name')
    if not name:
        flash('食材名稱為必填項目！', 'danger')
    else:
        Ingredient.create(name)
        flash('食材新增成功！', 'success')
    return redirect(url_for('ingredient.list_ingredients'))

@ingredient_bp.route('/ingredients/<int:id>/delete', methods=['POST'])
def delete_ingredient(id):
    if Ingredient.delete(id):
        flash('食材已刪除！', 'success')
    else:
        flash('刪除食材時發生錯誤。', 'danger')
    return redirect(url_for('ingredient.list_ingredients'))
