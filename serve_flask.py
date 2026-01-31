#!/usr/bin/env python3
"""
使用 Flask 框架提供静态 HTML 页面
需要先安装 Flask: pip install flask
"""

from flask import Flask, send_from_directory, abort
import os

app = Flask(__name__)

# 设置静态文件目录（当前目录）
STATIC_DIR = '.'

# 根路径返回 index.html（如果存在）
@app.route('/')
def home():
    if os.path.exists(os.path.join(STATIC_DIR, 'index.html')):
        return send_from_directory(STATIC_DIR, 'index.html')
    else:
        return "<h1>欢迎访问</h1><p>没有找到 index.html 文件</p>", 200

# 处理所有 .html 文件请求
@app.route('/<path:filename>')
def serve_html(filename):
    # 如果请求的是 .html 文件或者没有扩展名的文件
    if filename.endswith('.html'):
        # 直接返回对应的 HTML 文件
        if os.path.exists(os.path.join(STATIC_DIR, filename)):
            return send_from_directory(STATIC_DIR, filename)
        else:
            abort(404)
    elif '.' not in filename:
        # 如果没有扩展名，尝试添加 .html 后缀
        html_file = f"{filename}.html"
        if os.path.exists(os.path.join(STATIC_DIR, html_file)):
            return send_from_directory(STATIC_DIR, html_file)
        else:
            abort(404)
    else:
        # 其他静态文件（如 CSS、JS、图片等）
        if os.path.exists(os.path.join(STATIC_DIR, filename)):
            return send_from_directory(STATIC_DIR, filename)
        else:
            abort(404)

# 处理子目录中的文件
@app.route('/<path:subpath>/<path:filename>')
def serve_subdir_files(subpath, filename):
    file_path = os.path.join(subpath, filename)
    if os.path.exists(os.path.join(STATIC_DIR, file_path)):
        return send_from_directory(STATIC_DIR, file_path)
    else:
        abort(404)

# 自定义 404 错误页面
@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404 - 页面未找到</h1><p>请求的文件不存在</p>", 404

if __name__ == '__main__':
    print(f"服务器运行在 http://localhost:5001")
    print(f"静态文件目录: {os.path.abspath(STATIC_DIR)}")
    print("可以访问:")
    print("  - http://localhost:5001/english.html")
    print("  - http://localhost:5001/任意文件.html")
    print("按 Ctrl-C 停止服务器")
    app.run(debug=True, port=5001, host='0.0.0.0')