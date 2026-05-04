from flask import Blueprint, request, render_template, redirect, url_for, flash, abort
from app.models.recipe import Recipe
from app.models.ingredient import Ingredient

recipe_bp = Blueprint('recipe', __name__)

@recipe_bp.route('/', methods=['GET'])
@recipe_bp.route('/recipes', methods=['GET'])
def list_recipes():
    search_query = request.args.get('search', '')
    recipes = Recipe.get_all(search_query)
    return render_template('recipes/index.html', recipes=recipes, search_query=search_query)

@recipe_bp.route('/recipes/<int:id>', methods=['GET'])
def view_recipe(id):
    recipe = Recipe.get_by_id(id)
    if not recipe:
        abort(404)
    return render_template('recipes/detail.html', recipe=recipe)

@recipe_bp.route('/recipes/create', methods=['GET', 'POST'])
def create_recipe():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        steps = request.form.get('steps')
        ingredient_ids = request.form.getlist('ingredient_ids')
        
        if not title:
            flash('食譜標題為必填項目！', 'danger')
        else:
            Recipe.create(title, description, steps, ingredient_ids)
            flash('食譜新增成功！', 'success')
            return redirect(url_for('recipe.list_recipes'))
            
    ingredients = Ingredient.get_all()
    return render_template('recipes/create.html', ingredients=ingredients)

@recipe_bp.route('/recipes/<int:id>/edit', methods=['GET', 'POST'])
def edit_recipe(id):
    recipe = Recipe.get_by_id(id)
    if not recipe:
        abort(404)
        
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        steps = request.form.get('steps')
        ingredient_ids = request.form.getlist('ingredient_ids')
        
        if not title:
            flash('食譜標題為必填項目！', 'danger')
        else:
            Recipe.update(id, title, description, steps, ingredient_ids)
            flash('食譜更新成功！', 'success')
            return redirect(url_for('recipe.view_recipe', id=id))
            
    ingredients = Ingredient.get_all()
    # 擷取目前已選擇的食材 ID 列表
    selected_ingredient_ids = [ing['id'] for ing in recipe['ingredients']]
    return render_template('recipes/edit.html', recipe=recipe, ingredients=ingredients, selected_ingredient_ids=selected_ingredient_ids)

@recipe_bp.route('/recipes/<int:id>/delete', methods=['POST'])
def delete_recipe(id):
    if Recipe.delete(id):
        flash('食譜已刪除！', 'success')
    else:
        flash('刪除食譜時發生錯誤。', 'danger')
    return redirect(url_for('recipe.list_recipes'))
