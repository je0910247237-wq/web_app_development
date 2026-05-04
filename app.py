from flask import Flask
import sqlite3
import os

def create_app():
    app = Flask(__name__)
    
    # 基本設定
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    app.config['DATABASE'] = os.path.join(app.instance_path, 'database.db')
    
    # 確保 instance 資料夾存在
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 註冊 Blueprints
    from app.routes.recipe_routes import recipe_bp
    from app.routes.ingredient_routes import ingredient_bp
    app.register_blueprint(recipe_bp)
    app.register_blueprint(ingredient_bp)
    
    return app

def get_db_connection():
    """取得資料庫連線，並設定 row_factory"""
    # 我們假設 instance 已經在 app context 下建立
    # 這裡提供一個通用的 get_db_connection 供 scripts 使用
    conn = sqlite3.connect(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance', 'database.db'))
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """初始化資料庫 (會清空舊資料並套用 schema.sql)"""
    from flask import current_app
    # 建立 instance 資料夾
    os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance'), exist_ok=True)
    
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance', 'database.db')
    schema_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database', 'schema.sql')
    
    conn = sqlite3.connect(db_path)
    with open(schema_path, 'r', encoding='utf-8') as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()
    print("已成功初始化資料庫。")

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
