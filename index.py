from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)  # 启用跨域资源共享

# SQLite 数据库初始化
DATABASE = 'game_scores.db'

# 初始化数据库
def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    # 创建一个玩家得分表
    c.execute('''
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            score INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# 在启动时初始化数据库
init_db()

# 获取所有得分
@app.route('/api/scores', methods=['GET'])
def get_scores():
    """获取所有玩家的得分历史"""
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('SELECT * FROM scores ORDER BY score DESC')  # 按得分降序排列
    scores = c.fetchall()
    conn.close()
    
    return jsonify([{'id': row[0], 'name': row[1], 'score': row[2]} for row in scores])

# 提交得分
@app.route('/api/score', methods=['POST'])
def submit_score():
    """提交玩家的得分"""
    data = request.json
    name = data.get('name')
    score = data.get('score')

    if not name or score is None:
        return jsonify({'message': 'Invalid data! Name and score are required.'}), 400
    
    if not isinstance(score, int) or score < 0:
        return jsonify({'message': 'Invalid score! Score must be a non-negative integer.'}), 400

    # 将得分插入到数据库中
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('INSERT INTO scores (name, score) VALUES (?, ?)', (name, score))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Score submitted successfully!'}), 201

if __name__ == '__main__':
    app.run(debug=True)
