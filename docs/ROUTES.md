# 路由設計文件 (ROUTES) - 食譜收藏夾

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| --- | --- | --- | --- | --- |
| 首頁 (食譜列表) | GET | `/` 或 `/recipes` | `templates/recipes/index.html` | 顯示食譜清單，支援搜尋/過濾 |
| 建立食譜頁面 | GET | `/recipes/create` | `templates/recipes/create.html` | 顯示新增食譜表單 |
| 建立食譜 | POST | `/recipes/create` | — | 接收表單，存入資料庫，重導向至列表或詳情頁 |
| 食譜詳情 | GET | `/recipes/<int:id>` | `templates/recipes/detail.html` | 顯示單一食譜詳細內容 |
| 編輯食譜頁面 | GET | `/recipes/<int:id>/edit` | `templates/recipes/edit.html` | 顯示編輯食譜表單 |
| 更新食譜 | POST | `/recipes/<int:id>/edit` | — | 接收表單，更新資料庫，重導向至詳情頁 |
| 刪除食譜 | POST | `/recipes/<int:id>/delete`| — | 刪除指定食譜並重導向至列表頁 |
| 食材庫列表 | GET | `/ingredients` | `templates/ingredients/index.html` | 顯示所有食材庫中的食材 |
| 建立食材 | POST | `/ingredients/create` | — | 接收表單，新增食材，重導向至食材清單 |
| 刪除食材 | POST | `/ingredients/<int:id>/delete`| — | 刪除指定食材並重導向至食材清單 |

## 2. 每個路由的詳細說明

### 食譜相關 (Recipe Routes)

- **GET `/` 或 `/recipes`**
  - **輸入**：URL 參數 `?search=keyword` (可選)
  - **處理邏輯**：從資料庫查詢食譜列表，若有搜尋條件則進行過濾。
  - **輸出**：渲染 `recipes/index.html`，傳遞食譜列表資料。
  - **錯誤處理**：無特定錯誤。

- **GET `/recipes/create`**
  - **輸入**：無
  - **處理邏輯**：載入所有食材資料以便在表單中提供勾選/下拉選擇。
  - **輸出**：渲染 `recipes/create.html`，傳遞可選食材清單。

- **POST `/recipes/create`**
  - **輸入**：表單資料 (title, description, steps, ingredient_ids)
  - **處理邏輯**：驗證必填欄位，寫入 `recipe` 表，並將所選食材關聯寫入 `recipe_ingredient` 表。
  - **輸出**：成功後重導向至首頁 (`/recipes`) 或該食譜詳情頁。
  - **錯誤處理**：若資料驗證失敗，帶有錯誤訊息重新渲染 `recipes/create.html`。

- **GET `/recipes/<int:id>`**
  - **輸入**：食譜 ID
  - **處理邏輯**：依據 ID 從資料庫取得食譜詳細資訊，包含對應的食材列表。
  - **輸出**：渲染 `recipes/detail.html`，傳遞食譜與關聯食材資料。
  - **錯誤處理**：若找不到該 ID，返回 404 錯誤頁面或重導向首頁並提示錯誤。

- **GET `/recipes/<int:id>/edit`**
  - **輸入**：食譜 ID
  - **處理邏輯**：查詢該食譜的現有資料及其關聯的食材，同時載入所有可選食材以供修改。
  - **輸出**：渲染 `recipes/edit.html`，傳遞食譜原資料及所有食材。
  - **錯誤處理**：若找不到該 ID，返回 404 錯誤。

- **POST `/recipes/<int:id>/edit`**
  - **輸入**：食譜 ID 與表單資料 (title, description, steps, ingredient_ids)
  - **處理邏輯**：更新 `recipe` 表中的對應紀錄，並更新 `recipe_ingredient` 關聯 (可先刪除舊關聯再寫入新關聯)。
  - **輸出**：成功後重導向至食譜詳情頁 (`/recipes/<id>`)。
  - **錯誤處理**：驗證失敗則重新渲染編輯頁面並顯示錯誤。找不到 ID 則返回 404 錯誤。

- **POST `/recipes/<int:id>/delete`**
  - **輸入**：食譜 ID
  - **處理邏輯**：依據 ID 刪除 `recipe` 表紀錄 (因為設定了 ON DELETE CASCADE，關聯的 `recipe_ingredient` 也會自動刪除)。
  - **輸出**：刪除後重導向至首頁 (`/recipes`)。
  - **錯誤處理**：若找不到該 ID，返回 404 錯誤。

### 食材相關 (Ingredient Routes)

- **GET `/ingredients`**
  - **輸入**：無
  - **處理邏輯**：從資料庫查詢所有食材列表。
  - **輸出**：渲染 `ingredients/index.html`，傳遞食材清單資料。
  - **錯誤處理**：無。

- **POST `/ingredients/create`**
  - **輸入**：表單資料 (name)
  - **處理邏輯**：驗證食材名稱不為空，新增一筆紀錄至 `ingredient` 表。
  - **輸出**：成功後重導向至食材列表頁 (`/ingredients`)。
  - **錯誤處理**：若驗證失敗，可透過 flash message 提示並重導向回原頁。

- **POST `/ingredients/<int:id>/delete`**
  - **輸入**：食材 ID
  - **處理邏輯**：依據 ID 刪除指定食材 (ON DELETE CASCADE 會同時移除該食材與食譜的關聯)。
  - **輸出**：刪除後重導向至食材列表頁 (`/ingredients`)。
  - **錯誤處理**：若找不到該 ID，返回 404 錯誤。

## 3. Jinja2 模板清單

- `templates/base.html`
  - 角色：全站共用外框（包含 `<head>`、CSS 引入、共用導覽列、頁尾等）。
- `templates/recipes/index.html`
  - 角色：首頁 / 食譜列表頁，支援搜尋表單。
  - 繼承：`{% extends 'base.html' %}`
- `templates/recipes/create.html`
  - 角色：新增食譜表單頁面。
  - 繼承：`{% extends 'base.html' %}`
- `templates/recipes/detail.html`
  - 角色：單一食譜詳細內容（包含材料與步驟）。
  - 繼承：`{% extends 'base.html' %}`
- `templates/recipes/edit.html`
  - 角色：編輯食譜表單頁面。
  - 繼承：`{% extends 'base.html' %}`
- `templates/ingredients/index.html`
  - 角色：食材管理列表頁，包含新增食材的簡易表單。
  - 繼承：`{% extends 'base.html' %}`

## 4. 路由骨架程式碼

Python 檔案骨架已建立於 `app/routes/`：
- `app/routes/recipe_routes.py`
- `app/routes/ingredient_routes.py`
