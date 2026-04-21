# 系統流程圖與功能對照表 - 食譜收藏夾

本文件涵蓋了「食譜收藏夾」的使用者操作流程（User Flow）、系統處理資料流程（System Sequence Diagram），以及各功能對應的 URL 路由與 HTTP 方法。

## 1. 使用者流程圖 (User Flow)

描述使用者在系統中瀏覽、搜尋、新增、管理食譜及食材的操作路徑。

```mermaid
flowchart LR
    A([使用者造訪首頁]) --> B[首頁 - 食譜列表]
    B --> C{選擇操作}
    
    C -->|搜尋/過濾| D[檢視過濾後的食譜清單]
    
    C -->|點擊單一食譜| E[檢視食譜詳細頁面]
    E --> F{後續操作}
    F -->|點擊編輯| G[編輯食譜表單]
    F -->|點擊刪除| H[確認並刪除食譜]
    G --> I[儲存變更]
    I --> E
    H --> B
    
    C -->|點擊新增食譜| J[填寫新增食譜表單]
    J -->|填入步驟與挑選食材| K[送出並儲存]
    K --> B
    
    C -->|點擊食材管理| L[食材庫列表頁]
    L --> M{選擇操作}
    M -->|新增食材| N[填寫食材名稱並儲存]
    M -->|刪除食材| O[確認並刪除]
    N --> L
    O --> L
```

## 2. 系統序列圖 (Sequence Diagram)

以下以「使用者送出新增食譜」為例，描述從前端送出到資料存入資料庫的完整技術流向。

```mermaid
sequenceDiagram
    actor Chef as 廚師 (使用者)
    participant Browser as 瀏覽器
    participant Route as Flask Route
    participant Model as Database Model
    participant DB as SQLite

    Chef->>Browser: 填寫表單 (食譜名稱、步驟、勾選多項食材) 並送出
    Browser->>Route: 發送 POST /recipes/create 請求
    Route->>Model: 提取表單資料，呼叫 Model 新增邏輯
    
    Note over Model,DB: 處理多對多關聯儲存
    Model->>DB: 1. INSERT INTO recipes (寫入食譜基本資料)
    DB-->>Model: 取得新增的 recipe_id
    Model->>DB: 2. INSERT INTO recipe_ingredients (依序寫入關聯表)
    DB-->>Model: 寫入完成
    
    Model-->>Route: 業務邏輯處理完畢
    Route-->>Browser: 返回 HTTP 302 重導向 (Redirect) 至食譜列表或詳情首頁
    Browser-->>Chef: 畫面重新載入，顯示成功訊息及剛新增的食譜
```

## 3. 功能清單對照表

對應 PRD 與架構設計，以下整理出本專案核心功能的路由規劃。

| 功能區塊 | 操作行為 | URL 路徑 | HTTP 方法 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| **食譜功能** | 顯示所有食譜 | `/` 或 `/recipes` | GET | 首頁，顯示食譜清單，可附帶搜尋查詢參數 |
| **食譜功能** | 顯示詳細內容 | `/recipes/<id>` | GET | 顯示單一食譜的材料清單、完整步驟與標籤 |
| **食譜功能** | 顯示新增表單 | `/recipes/create` | GET | 呈現新增食譜的空白 HTML 表單 |
| **食譜功能** | 處理新增資料 | `/recipes/create` | POST | 接收前端表單並將食譜與食材寫入資料庫 |
| **食譜功能** | 顯示編輯表單 | `/recipes/<id>/edit` | GET | 呈現預先載入舊資料的食譜編輯表單 |
| **食譜功能** | 處理變更資料 | `/recipes/<id>/edit` | POST | 更新資料庫中的食譜資訊與對應的食材關聯 |
| **食譜功能** | 執行刪除動作 | `/recipes/<id>/delete`| POST | 安全性考量，使用 POST 刪除特定食譜 |
| **食材管理** | 預覽已有食材 | `/ingredients` | GET | 顯示目前食材庫中的所有可用食材 |
| **食材管理** | 新增未知食材 | `/ingredients/create` | POST | 加入一筆新食材至系統供未來直接選用 |
| **食材管理** | 刪除閒置食材 | `/ingredients/<id>/delete`| POST | 刪除不再需要的自訂食材 |
