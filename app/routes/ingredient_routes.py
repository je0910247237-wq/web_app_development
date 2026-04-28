"""Route skeleton for ingredient related endpoints.
All functions contain only the route decorator, signature and a docstring describing the purpose.
Implementation (database calls, template rendering, redirects) will be added later.
"""

from flask import Blueprint, request, render_template, redirect, url_for, abort

# Blueprint for ingredient routes
ingredient_bp = Blueprint('ingredient', __name__)

@ingredient_bp.route('/ingredients', methods=['GET'])
def list_ingredients():
    """列出所有食材
    - 輸入: 無
    - 處理: 取得所有食材 (Ingredient.get_all) (未實作)
    - 輸出: 渲染 `templates/ingredients/index.html`
    - 錯誤處理: 無特別錯誤
    """
    pass

@ingredient_bp.route('/ingredients/create', methods=['POST'])
def create_ingredient():
    """建立新食材
    - 輸入: 表單欄位 `name`
    - 處理: 呼叫 Ingredient.create
    - 輸出: 成功後 `redirect` 回食材列表
    - 錯誤處理: 資料驗證失敗重新呈現表單
    """
    pass

@ingredient_bp.route('/ingredients/<int:id>/delete', methods=['POST'])
def delete_ingredient(id):
    """刪除指定食材
    - 輸入: URL 參數 `id`
    - 處理: 呼叫 Ingredient.delete
    - 輸出: `redirect` 回食材列表
    - 錯誤處理: 若找不到返回 404
    """
    pass
