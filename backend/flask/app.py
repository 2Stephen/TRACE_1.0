# -*- coding: utf-8 -*-
import os
from flask import Flask, request, url_for, jsonify
from flask_cors import CORS
import img_search as kernel
import pandas as pd
from gevent import pywsgi

app = Flask(__name__, static_folder='results')
CORS(app)  # 允许跨域请求
model = kernel.load()

global pos


# 接收前端的图片数据
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    file.save('photos\\' + file.filename)
    # 调用模型进行图片搜索
    kernel.segment(file.filename, pos)
    return '上传成功'


# 上传待搜索的书架位置
@app.route('/uploadLocation', methods=['POST'])
def uploadLocation():
    global pos
    # 将json格式data转换成字典格式
    data = request.get_json()
    pos = data['sectionData']
    return '上传路径成功'


@app.route('/getExampleImages', methods=['GET'])
def getExampleImages():
    if not os.path.exists(os.path.join('results', 'example')):
        return jsonify({'image_urls': []})
    example_image_dir = os.path.join('results', 'example')

    # 从目录中获取所有图片文件名
    image_files = [f for f in os.listdir(example_image_dir) if os.path.isfile(os.path.join(example_image_dir, f))]

    base_url = request.host_url  # 获取如 'http://localhost:5000/' 的基础 URL

    # 生成每张图片的 URL，使用 'static' endpoint
    image_urls = [url_for('static', filename=f'example/{image}') for image in image_files]
    # 为image_urls中的每个图片添加base_url
    image_urls = [base_url + image for image in image_urls]

    # 返回 JSON 响应，包含图片的 URL
    return jsonify({'image_urls': image_urls})

@app.route('/getFalseImages', methods=['GET'])
def getFalseImages():
    # 指定存放图片的目录
    # 如果不包含路径，则直接返回无错误书籍
    if not os.path.exists(os.path.join('results', 'misplaced_books')):
        return jsonify({'image_urls': []})
    false_image_dir = os.path.join('results', 'misplaced_books')

    # 从目录中获取所有图片文件名
    image_files = [f for f in os.listdir(false_image_dir) if os.path.isfile(os.path.join(false_image_dir, f))]

    base_url = request.host_url  # 获取如 'http://localhost:5000/' 的基础 URL

    # 生成每张图片的 URL，使用 'static' endpoint
    image_urls = [url_for('static', filename=f'misplaced_books/{image}') for image in image_files]
    # 为image_urls中的每个图片添加base_url
    image_urls = [base_url + image for image in image_urls]

    # 返回 JSON 响应，包含图片的 URL
    return jsonify({'image_urls': image_urls})


@app.route('/getTrueImages', methods=['GET'])
def getTrueImages():
    # 指定存放图片的目录
    true_image_dir = os.path.join('results', 'correct_books')

    # 从目录中获取所有图片文件名
    image_files = [f for f in os.listdir(true_image_dir) if os.path.isfile(os.path.join(true_image_dir, f))]

    base_url = request.host_url  # 获取如 'http://localhost:5000/' 的基础 URL

    # 生成每张图片的 URL，使用 'static' endpoint
    image_urls = [url_for('static', filename=f'correct_books/{image}') for image in image_files]
    # 为image_urls中的每个图片添加base_url
    image_urls = [base_url + image for image in image_urls]

    # 返回 JSON 响应，包含图片的 URL
    return jsonify({'image_urls': image_urls})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
