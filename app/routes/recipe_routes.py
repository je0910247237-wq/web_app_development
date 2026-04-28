"""Route skeleton for recipe related endpoints.
All functions contain only the route decorator, signature and a docstring describing the purpose.
Implementation (database calls, template rendering, redirects) will be added later.
"""

from flask import Blueprint, request, render_template, redirect, url_for, abort

# Blueprint for recipe routes
recipe_bp = Blueprint('recipe', __name__)

@recipe_bp.route('/', methods=['GET'])
def list_recipes():
    """列出所有食譜
    - 輸入: 無
    - 處理: 取得所有食譜 (Recipe.get_all) (未實作)
    - 輸出: 渲染 `templates/recipes/index.html`
    - 錯誤處理: 無特別錯誤
    """
    pass

@recipe_bp.route('/recipes/<int:id>', methods=['GET'])
def view_recipe(id):
    """顯示單一食譜詳細資訊
    - 輸入: URL 參數 `id`
    - 處理: 透過 Recipe.get_by_id 取得食譜
    - 輸出: 渲染 `templates/recipes/detail.html`
    - 錯誤處理: 若找不到返回 404
    """
    pass

@recipe_bp.route('/recipes/create', methods=['GET'])
def create_recipe_form():
    """顯示新增食譜的表單
    - 輸入: 無
    - 輸出: 渲染 `templates/recipes/create.html`
    """
    pass

@recipe_bp.route('/recipes/create', methods=['POST'])
def create_recipe():
    """處理表單提交，建立食譜
    - 輸入: 表單欄位 `title`, `description`, `steps`, `ingredient_ids`
    - 處理: 呼叫 Recipe.create
    - 輸出: 成功後 `redirect` 到食譜列表
    - 錯誤處理: 資料驗證失敗重新呈現表單
    """
    pass

@recipe_bp.route('/recipes/<int:id>/edit', methods=['GET'])
def edit_recipe_form(id):
    """顯示編輯食譜表單，預載入現有資料
    - 輸入: URL 參數 `id`
    - 輸出: 渲染 `templates/recipes/edit.html`
    """
    pass

@recipe_bp.route('/recipes/<int:id>/edit', methods=['POST'])
def update_recipe(id):
    """處理編輯表單，更新食譜
    - 輸入: 表單欄位與 URL `id`
    - 處理: 呼叫 Recipe.update
    - 輸出: 成功後 `redirect` 到食譜詳細頁
    - 錯誤處理: 驗證失敗重新渲染表單
    """
    pass

@recipe_bp.route('/recipes/<int:id>/delete', methods=['POST'])
def delete_recipe(id):
    """刪除指定食譜
    - 輸入: URL 參數 `id`
    - 處理: 呼叫 Recipe.delete
    - 輸出: `redirect` 回食譜列表
    - 錯誤處理: 若找不到返回 404
    """
    pass
