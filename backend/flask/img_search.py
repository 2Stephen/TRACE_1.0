# -*- coding: utf-8 -*-

import argparse
import os
import glob
from PIL import Image, ImageDraw
import torch
import cn_clip.clip as clip
import tqdm
import pandas as pd
import matplotlib.pyplot as plt
import time
import os.path
import cv2
import numpy as np
import os
from ultralytics import YOLO
from pathlib import Path
import faiss
import shutil
import matplotlib.gridspec as gridspec
from cn_clip.clip import load_from_name, available_models

#%%
global model, preprocess, device, model_seg, args
path = r'E:\bookspines_project\back_py\flaskProject'


def load():
    global model, preprocess, device, model_seg, args

    args = Args()
    args.mode = 'predict'
    # YOLO模型加载
    model_seg = YOLO(args.yolo_best_path)
    print('YOLO模型加载完毕')
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, preprocess = load_from_name("ViT-H-14", device=device, download_root='./')
    print('CLIP模型加载完毕')
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 这里设置为支持中文的字体
    plt.rcParams['axes.unicode_minus'] = False  # 用于正常显示负号


#%%
# 设置参数
class Args:
    # 图像大小
    input_size = 640
    # yolo最佳模型
    yolo_best_path = os.path.join(path, 'models/best.pt')

    # 搭建库的数据集路径
    database_dir = os.path.join(path, r'database')
    # 数据库图片分割后的数据集路径
    database_by_yolo = os.path.join(path, r'segmented_img')

    # # 数据库图片分割后数据增强的数据集路径
    # database_dir_aug = r'D:\programme\anaconda3\jupyterfile\guochuang_final\output\database_dir_aug'
    # # 数据库图片分割后的位置路径
    # database_shelf_location = r'D:\programme\anaconda3\jupyterfile\guochuang_final\dataset\location'
    # # 数据库图片分割后的位置信息文件
    # database_shelf_location_csv = r"D:\programme\anaconda3\jupyterfile\guochuang_final\dataset\location\database_shelf_locations2.xlsx"
    # # 数据库图像特征文件路径
    # database_feature_path = r'D:\programme\anaconda3\jupyterfile\guochuang_final\dataset\feature'

    # 数据库图像特征文件
    database_feature = os.path.join(path, r'models\corpus_feature_dict.npy')
    # # 数据库索引文件路径
    # database_index_path = r'D:\programme\anaconda3\jupyterfile\guochuang_final\dataset\index'
    # 数据库索引文件
    database_index = os.path.join(path, r'models\faiss_index_ivf.index')

    test_bbox_file = os.path.join(path, r'models\test_bounding_boxes.npy')
    # 待测图片路径
    test_image_dir = os.path.join(path, r'photos')
    # 待测图片分割完后的路径
    test_image_by_yolo = os.path.join(path, r'segment_by_yolo')
    # # 待测图片的位置信息
    test_shelf_location = os.path.join(path, r'location')
    test_shelf_location_csv = os.path.join(path, r'location\test_shelf_locations.xlsx')
    # 测试图片匹配结果存储路径
    save_dir = os.path.join(path, r'results')
    test_by_yoloBIG = os.path.join(path, r'test_by_yolo_BIG')
    # 特征提取模型
    model_name = 'clip'  # 可选 resnet50, resnet152, clip
    #数据库图片的边界框信息文件
    base_bbox_file= os.path.join(path, r'models\bounding_boxes.npy')

    # 搜寻前k个相似图片
    topk = 2

    # 选择当前模式
    mode = 'extract'  # 'extract' 表示提取特征，'predict' 表示匹配相似图片

    # 匹配算法
    index_type = 'ivf'

args = Args()


#%%


# ## 实例分割：target_extraction_by_yolov8


def target_extraction_by_yolov8(args, pos, datapath,mode=args.mode,batch_size=6):
    if args.mode == 'extract':
        # YOLO模型加载
        model_seg = YOLO(args.yolo_best_path)
        print('YOLO模型加载完毕')
        # 获取所有图像路径
        image_paths = [os.path.join(datapath, img) for img in os.listdir(datapath) if img.endswith(('.jpg', '.png', '.jpeg'))]
        # 将数据分成批次
        total_images = len(image_paths)
        batches = [image_paths[i:i + batch_size] for i in range(0, total_images, batch_size)]
        print(f'总共有 {total_images} 张图片，批次大小为 {batch_size}，将分为 {len(batches)} 个批次进行处理')
        # 用于存储边界框数据的字典
        bbox_data = {}
        for batch_idx, batch in enumerate(batches):
            print(f'正在处理第 {batch_idx + 1} 批次，共 {len(batch)} 张图片')
            print(batch_idx)
            # 批量加载图片进行分割
            results = model_seg(batch)  # 传入当前批次的图片列表
            print('批次实例分割完成')
            # 处理分割结果
            for result in results:
                # 加载原始图像
                image_path = result.path  # Path to the image
                original_image = cv2.imread(image_path)
                image_name = Path(image_path).stem  # 提取文件名，不包括扩展名
                # 获取图像的高度和宽度
                height, width, _ = original_image.shape
                # 检查结果中是否存在掩码
                if result.masks is None:
                    print(f"No masks found for {image_name}. Saving the original image...")
                    continue
                # 迭代每个检测(对象)
                for i, mask in enumerate(result.masks.data):
                    object_name = f"{image_name}_object_{i}"
                    # 获取当前对象的掩码和边界框
                    obj_mask = mask.cpu().numpy()  # Convert mask to NumPy array (H, W)
                    # 将布尔掩码转换为8位无符号整型(OpenCV需要)
                    obj_mask = (obj_mask * 255).astype(np.uint8)
                    # 确保蒙版大小与原始图像大小匹配
                    if obj_mask.shape[0] != height or obj_mask.shape[1] != width:
                        obj_mask = cv2.resize(obj_mask, (width, height), interpolation=cv2.INTER_NEAREST)
                    # 将蒙版直接应用于原始图像以提取对象
                    masked_obj = cv2.bitwise_and(original_image, original_image, mask=obj_mask)
                    # 根据被遮罩对象的边界框裁剪它
                    obj_bbox = result.boxes.xyxy[i].cpu().numpy().astype(int)  # Bounding box in (xmin, ymin, xmax, ymax)
                    xmin, ymin, xmax, ymax = obj_bbox
                    # 存储当前对象的边界框信息，使用 object_name 作为键
                    bbox_data[object_name] = [xmin, ymin, xmax, ymax]
                    cropped_obj = masked_obj[ymin:ymax, xmin:xmax]
                    # 存储分割对象
                    if mode == 'extract':
                        output_path = os.path.join(r'D:\programme\anaconda3\jupyterfile\guochuang_final\output\database_by_yolo_for_boxes', f"{image_name}_object_{i}.jpg")
                    elif mode == 'predict':
                        output_path = os.path.join(args.test_image_by_yolo, f"{image_name}_object_{i}.jpg")
                    cv2.imwrite(output_path, cropped_obj)
                # 存大结果
                result.save(filename=os.path.join(r'D:\programme\anaconda3\jupyterfile\guochuang_final\output\database_by_yolo_BIG2',
                                                  f"{image_name}_result.jpg"))


            print(f'批次 {batch_idx + 1} 的实例分割结果已存储完毕')
        # 将边界框信息保存到 .npy 文件
        np.save(r'D:\programme\anaconda3\jupyterfile\guochuang_final\dataset\boxes\baese_bounding_boxes.npy', bbox_data)
        print("边界框信息已保存到 base_bounding_boxes.npy")
    elif args.mode == 'predict':
        # 先用yolo对待测图片进行分割
        model_seg = YOLO(args.yolo_best_path)
        print('模型加载完毕')
        results = model_seg(datapath)  # 传入当前批次的图片列表
        # 用于存储边界框数据的字典
        bbox_data = {}
        # 处理分割结果
        for result in results:
            # 加载原始图像
            image_path = result.path  # Path to the image
            original_image = cv2.imread(image_path)
            image_name = Path(image_path).stem  # 提取文件名，不包括扩展名
            # 获取图像的高度和宽度
            height, width, _ = original_image.shape
            # 检查结果中是否存在掩码
            if result.masks is None:
                print(f"No masks found for {image_name}. Saving the original image...")
                continue
            # 迭代每个检测(对象)
            for i, mask in enumerate(result.masks.data):
                object_name = f"{image_name}_object_{i}"
                # 写入test shelf location表格
                excel_file_path = r'location/test_shelf_locations.xlsx'
                df = pd.read_excel(excel_file_path)

                # 创建一个新的DataFrame并追加
                new_data = pd.DataFrame({'image_path': [object_name + ".jpg"], 'shelf_location': [pos]})
                df = pd.concat([df, new_data], ignore_index=True)

                # 将更新后的DataFrame写回Excel文件
                df.to_excel(excel_file_path, index=False)
                # 获取当前对象的掩码和边界框
                obj_mask = mask.cpu().numpy()  # Convert mask to NumPy array (H, W)
                # 将布尔掩码转换为8位无符号整型(OpenCV需要)
                obj_mask = (obj_mask * 255).astype(np.uint8)
                # 确保蒙版大小与原始图像大小匹配
                if obj_mask.shape[0] != height or obj_mask.shape[1] != width:
                    obj_mask = cv2.resize(obj_mask, (width, height), interpolation=cv2.INTER_NEAREST)
                # 将蒙版直接应用于原始图像以提取对象
                masked_obj = cv2.bitwise_and(original_image, original_image, mask=obj_mask)
                # 根据被遮罩对象的边界框裁剪它
                obj_bbox = result.boxes.xyxy[i].cpu().numpy().astype(int)  # Bounding box in (xmin, ymin, xmax, ymax)
                xmin, ymin, xmax, ymax = obj_bbox
                # 存储当前对象的边界框信息，使用 object_name 作为键
                bbox_data[object_name] = [xmin, ymin, xmax, ymax]
                cropped_obj = masked_obj[ymin:ymax, xmin:xmax]
                # 存储分割对象
                if mode == 'extract':
                    output_path = os.path.join(args.database_by_yolo, f"{image_name}_object_{i}.jpg")
                elif mode == 'predict':
                    output_path = os.path.join(args.test_image_by_yolo, f"{image_name}_object_{i}.jpg")
                cv2.imwrite(output_path, cropped_obj)
            # 存大结果
            result.save(
                filename=os.path.join(args.test_by_yoloBIG, f"{image_name}_result.jpg"))
        print('实例分割存储完毕')
        # 将边界框信息保存到 .npy 文件
        np.save(args.test_bbox_file, bbox_data)
        print("边界框信息已保存到 test_bounding_boxes.npy")


def extract_feature_by_CLIP(model, preprocess, file):
    image = preprocess(Image.open(file)).unsqueeze(0).to(device)
    with torch.no_grad():
        vec = model.encode_image(image)
        vec = vec.squeeze(0).cpu().numpy()
    return vec


def load_shelf_locations(file_path):
    df = pd.read_excel(file_path)
    shelf_location = {row['image_path']: row['shelf_location'] for index, row in df.iterrows()}
    print(shelf_location)
    return shelf_location


def search_with_faiss(args, model, preprocess, test_images, shelf_location, index_type='ivf'):
    # 加载特征字典以保留位置信息
    # 加载特征数据库
    allVectors = np.load(args.database_feature, allow_pickle=True)
    allVectors = allVectors.item()
    #     print(allVectors.keys())
    # 加载索引
    index_file_name = args.database_index
    index = faiss.read_index(index_file_name)

    # 使用 GPU
    res = faiss.StandardGpuResources()
    index = faiss.index_cpu_to_gpu(res, 0, index)
    #     print(index)
    result = {}
    for img_file in tqdm.tqdm(test_images):
        #         print(img_file)
        if args.model_name == 'clip':
            features = extract_feature_by_CLIP(model, preprocess, img_file)
            features = features / np.linalg.norm(features)  # 归一化

            features = np.array([features])  # 转换为二维数组

            # 使用 FAISS 进行最近邻搜索
            index.nprobe = 1000
            D, I = index.search(features, args.topk)  # 返回 topk 最近邻的索引

            simImages, simScores, simLocations = [], [], []
            for ind in I[0]:  # I[0] 是当前查询的最近邻索引
                # allVectors.keys()是名字
                simImages.append(list(allVectors.keys())[ind])
                simScores.append(D[0][np.where(I[0] == ind)[0][0]])  # 获取对应的距离
                simLocations.append(allVectors[list(allVectors.keys())[ind]]['shelf_location'])
                # print(list(allVectors.keys())[ind], D[0][np.where(I[0] == ind)[0][0]],allVectors[list(allVectors.keys())[ind]]['shelf_location'])
                # print(allVectors)
            # 添加被检测图像的信息，包括位置
            result[img_file] = {
                'query_image': img_file,
                'shelf_location': shelf_location.get(img_file.split('\\')[-1], 'Unknown'),  # 现在从 shelf_location 获取位置信息
                'similar_images': simImages,
                'similar_scores': simScores,
                'similar_locations': simLocations,
            }

    return result


# ### setAxes:绘制相似图片

# In[8]:


def setAxes(ax, image, query=False, **kwargs):
    value = kwargs.get('value', None)
    if query:
        ax.set_xlabel("Query Image\n{0}".format(os.path.basename(image)), fontsize=20)
        ax.xaxis.label.set_color('red')
    else:
        ax.set_xlabel("score={1:1.3f}\n{0}".format(os.path.basename(image), value), fontsize=20)
        ax.xaxis.label.set_color('blue')
    ax.set_xticks([])
    ax.set_yticks([])


def find_shelf_image(result_image_name, shelf_images_dir):
    """根据分割结果的文件名，找到对应的书架图片。"""
    shelf_image_prefix = result_image_name.split("_object_")[0]
    for img_path in Path(shelf_images_dir).glob(f"{shelf_image_prefix}*.jpg"):
        return str(img_path)  # 返回找到的书架图片路径
    return None

def load_bounding_boxes(bbox_file):
    """加载存储的边界框信息（.npy 文件）"""
    return np.load(bbox_file, allow_pickle=True).item()


def draw_bounding_box_on_shelf(shelf_image, bbox):
    """在书架图片上绘制书籍的边界框。"""
    draw = ImageDraw.Draw(shelf_image)
    xmin, ymin, xmax, ymax = bbox
    draw.rectangle([xmin, ymin, xmax, ymax], outline="red", width=30)
    return shelf_image


def plotSimilarImages(args, image, simImages, simValues, simLocations, query_shelf_location):
    """
    比较待测图片和最相似的两张图片的位置信息，确定书本摆放是否正确，并保存图像。
    :param args: 参数对象
    :param image: 待测图片路径
    :param simImages: 最相似图片的路径列表
    :param simValues: 最相似图片的相似度分数列表
    :param simLocations: 最相似图片的位置列表
    :param query_shelf_location: 待测图片的书架位置信息
    """
    # 加载测试图片的边界框信息
    test_bbox_data = load_bounding_boxes(args.test_bbox_file)

    # 当前图片的名字（无扩展名）
    result_image_name = os.path.basename(image).split('.')[0]

    # 寻找当前书本的书架图片和边界框
    shelf_image_path = find_shelf_image(result_image_name, args.test_image_dir)
    print(shelf_image_path)

    if shelf_image_path and result_image_name in test_bbox_data:
        bbox = test_bbox_data[result_image_name]
    else:
        print(f"未找到当前书本的书架图片或边界框信息: {result_image_name}")
        return

    # 判断位置是否相同
    if query_shelf_location in simLocations[:2]:  # 如果位置相同，说明摆放正确
        print(f"书本 {result_image_name} 摆放正确。")

        # 创建 correct_books 文件夹
        correct_folder = os.path.join(args.save_dir, "correct_books")
        if not os.path.exists(correct_folder):
            os.makedirs(correct_folder)

        # 找到位置相同的书本（可能是第一本或第二本相似图片）
        if query_shelf_location == simLocations[0]:
            similar_image_name = os.path.basename(simImages[0]).split('.')[0]
        else:
            similar_image_name = os.path.basename(simImages[1]).split('.')[0]

        # 查找匹配书本的书架图片及其边界框
        similar_shelf_image_path = find_shelf_image(similar_image_name, args.database_dir)
        sim_bbox_data = load_bounding_boxes(args.base_bbox_file)
        # print(sim_bbox_data)
        if similar_shelf_image_path and similar_image_name in sim_bbox_data:
            sim_bbox = sim_bbox_data[similar_image_name]

            # 绘制图像：当前书本、当前书架位置、匹配书本的位置
            fig = plot_book_and_shelf(args, image, shelf_image_path, bbox, query_shelf_location)

            # 子图3：匹配到的相似书本在书架上的位置
            similar_shelf_image = Image.open(similar_shelf_image_path).copy()
            similar_shelf_image_with_bbox = draw_bounding_box_on_shelf(similar_shelf_image, sim_bbox)

            ax3 = fig.add_subplot(1, 3, 3)
            ax3.set_title("真正所属书架")
            ax3.set_xticks([])
            ax3.set_yticks([])
            plt.imshow(similar_shelf_image_with_bbox)
            ax3.text(0.5, -0.1, query_shelf_location, ha='center', fontsize=20, transform=ax3.transAxes)

            # 保存图像
            save_fig_path = os.path.join(correct_folder, f"{result_image_name}_correct.png")
            fig.savefig(save_fig_path)
            plt.close(fig)
            print(f"已保存正确摆放图像: {save_fig_path}")
        else:
            print(f"未找到相似书本的书架图片或边界框信息")
    else:
        print(f"书本 {result_image_name} 摆放错误。")

        # 创建 misplaced_books 文件夹
        misplaced_folder = os.path.join(args.save_dir, "misplaced_books")
        if not os.path.exists(misplaced_folder):
            os.makedirs(misplaced_folder)

        # 使用最接近的相似图片展示书本的错误摆放位置
        similar_image_name = os.path.basename(simImages[0]).split('.')[0]

        # 查找匹配书本的书架图片及其边界框
        similar_shelf_image_path = find_shelf_image(similar_image_name, args.database_dir)
        sim_bbox_data = load_bounding_boxes(args.base_bbox_file)

        if similar_shelf_image_path and similar_image_name in sim_bbox_data:
            sim_bbox = sim_bbox_data[similar_image_name]

            # 绘制图像：当前书本、当前书架位置、最接近的相似书本的位置
            fig = plot_book_and_shelf(args, image, shelf_image_path, bbox, query_shelf_location)

            # 子图3：最接近的相似书本在书架上的位置
            similar_shelf_image = Image.open(similar_shelf_image_path).copy()
            similar_shelf_image_with_bbox = draw_bounding_box_on_shelf(similar_shelf_image, sim_bbox)

            ax3 = fig.add_subplot(1, 3, 3)
            ax3.set_title("真正所属书架")
            ax3.set_xticks([])
            ax3.set_yticks([])
            plt.imshow(similar_shelf_image_with_bbox)
            ax3.text(0.5, -0.1, simLocations[0], ha='center', fontsize=20, transform=ax3.transAxes)

            # 保存图像
            save_fig_path = os.path.join(misplaced_folder, f"{result_image_name}_misplaced.png")
            fig.savefig(save_fig_path)
            plt.close(fig)
            print(f"已保存错误摆放图像: {save_fig_path}")
        else:
            print(f"未找到相似书本的书架图片或边界框信息。")


def plot_book_and_shelf(args, image, shelf_image_path, bbox, shelf_location):
    """
    绘制当前待检测书本及其在书架上的位置图，并调整子图大小比例。
    """
    fig = plt.figure(figsize=(15, 5))  # 整体图大小
    fig.suptitle(f'TRACE', fontsize=40)
    # 调整子图与标题之间的距离，top=0.85表示标题位置
    plt.subplots_adjust(top=0.75)  # 这里调整标题和子图之间的距离，0.75可以根据需求调整

    # 使用 GridSpec 来调整子图的比例
    gs = gridspec.GridSpec(1, 3, width_ratios=[1, 2, 2])  # 子图1占1份宽度，子图2和子图3各占2份宽度

    # 子图1：展示当前书本的分割图（较小）
    ax1 = fig.add_subplot(gs[0])
    img = Image.open(image)
    ax1.set_title("当前检测书本")
    ax1.set_xticks([])
    ax1.set_yticks([])
    plt.imshow(img)
    ax1.text(0.5, -0.1, shelf_location, ha='center', fontsize=20, transform=ax1.transAxes)

    # 子图2：展示书本在书架上的位置，并绘制边界框（较大）
    shelf_image = Image.open(shelf_image_path).copy()
    shelf_image_with_bbox = draw_bounding_box_on_shelf(shelf_image, bbox)

    ax2 = fig.add_subplot(gs[1])
    ax2.set_title("当前所在书架")
    ax2.set_xticks([])
    ax2.set_yticks([])
    plt.imshow(shelf_image_with_bbox)
    ax2.text(0.5, -0.1, shelf_location, ha='center', fontsize=20, transform=ax2.transAxes)

    return fig


def getSimilarMatrix(vectors_dict):
    v = np.array([value['features'] for value in vectors_dict.values()])  # 确保提取特征
    numerator = np.matmul(v, v.T)  # 分子
    denominator = np.matmul(np.linalg.norm(v, axis=1, keepdims=True), np.linalg.norm(v, axis=1, keepdims=True).T)  # 分母
    sim = numerator / denominator
    keys = list(vectors_dict.keys())
    # print(sim)

    return sim, keys


def baoli(args):
    allVectors = np.load(args.database_feature, allow_pickle=True)
    allVectors = allVectors.item()

    for img_file in tqdm.tqdm(test_images):
        if args.model_name == 'clip':
            features = extract_feature_by_CLIP(model, preprocess, img_file)
            # 添加位置信息，默认为"Unknown"
            shelf_loc = shelf_location.get(img_file, 'Unknown') if shelf_location else 'Unknown'
            allVectors[img_file] = {
                'features': features,
                'shelf_location': shelf_loc
            }

    sim, keys = getSimilarMatrix(allVectors)
    result = {}
    # print('hhh')
    for image_file in tqdm.tqdm(test_images):
        # print(image_file)
        # print(f'sorting most similar images as {image_file}')

        index = keys.index(image_file)
        sim_vec = sim[index]
        # 获取前 topk + 1 个相似图片（包括自身）
        indexs = np.argsort(sim_vec)[::-1]  # 先按相似度排序，从大到小
        simImages, simScores, simLocations = [], [], []
        for ind in indexs:
            if keys[ind] != image_file:  # 过滤掉被检测的图片
                simImages.append(keys[ind])
                simScores.append(sim_vec[ind])
                simLocations.append(allVectors[keys[ind]]['shelf_location'])  # 获取位置信息
            if len(simImages) >= args.topk:  # 确保只获取 topk 个相似图像
                break

        result[image_file] = (simImages, simScores, simLocations)  # 将位置信息也存入结果
    return result


#%%

def segment(img_name, pos):
    # 第二阶段：图像检索

    # 读取 Excel 文件
    excel_file_path = args.test_shelf_location_csv
    df = pd.read_excel(excel_file_path)

    # 保留表头，删除所有数据
    df = df.iloc[0:0]  # 只保留表头，清空所有行数据

    # 将结果保存回 Excel 文件
    df.to_excel(excel_file_path, index=False)
    # 删除之前的缓存
    # 获取目标目录路径

    save_dir_mistake = os.path.join(args.save_dir, 'misplaced_books')
    save_dir_correct = os.path.join(args.save_dir, 'correct_books')
    seg_dir = args.test_image_by_yolo

    # 遍历 save_dir_mistake 中的所有内容
    for item in os.listdir(save_dir_mistake):
        item_path = os.path.join(save_dir_mistake, item)
        # 如果是文件或符号链接，直接删除
        if os.path.isfile(item_path) or os.path.islink(item_path):
            os.remove(item_path)
        # 如果是目录，递归删除
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)

    # 遍历 save_dir_correct 中的所有内容
    for item in os.listdir(save_dir_correct):
        item_path = os.path.join(save_dir_correct, item)  # Corrected to use save_dir_correct
        # 如果是文件或符号链接，直接删除
        if os.path.isfile(item_path) or os.path.islink(item_path):
            os.remove(item_path)
        # 如果是目录，递归删除
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)

    # 遍历 seg_dir 中的所有内容
    for item in os.listdir(seg_dir):
        item_path = os.path.join(seg_dir, item)
        # 如果是文件或符号链接，直接删除
        if os.path.isfile(item_path) or os.path.islink(item_path):
            os.remove(item_path)
        # 如果是目录，递归删除
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)

    if args.mode == 'predict':
        start_time_extract = time.time()  # 记录开始时间

        target_extraction_by_yolov8(args, pos,
                                    os.path.join(args.test_image_dir, img_name),
                                    'predict')
        print(f'用 clip 模型来提取特征')

        end_time_extract = time.time()  # 记录结束时间
        print(f"Time taken to extract features: {end_time_extract - start_time_extract:.2f} seconds")
        match()
    else:
        print('模式错误')


# ## 生成位置信息

#%%

def match():
    start_time_match = time.time()  # 记录开始时间

    print(f'use preyrained model {args.model_name} to search {args.topk} similar images from corpus')

    # 加载测试图片
    test_images = glob.glob(os.path.join(args.test_image_by_yolo, '*.jpg'))

    # 在主函数中加载位置信息
    shelf_location = {}
    if args.test_shelf_location:  # 检查是否提供了路径
        if os.path.exists(args.test_shelf_location_csv):
            shelf_location = load_shelf_locations(args.test_shelf_location_csv)
            print(shelf_location)
        else:
            print("Warning: Text shelf location file not found.")
    else:
        print("Warning: No text shelf location file provided.")

    args.index_type = 'ivf'
    # 使用索引进行搜索，传递 shelf_location 参数
    if args.index_type == 'ivf':
        result = search_with_faiss(args, model, preprocess, test_images, shelf_location, index_type='ivf')  # 或 'flat'

        #         # 生成测试图片的位置信息CSV
        #         generate_test_location_csv(args, result)

        for img_file in test_images:
            query_result = result.get(img_file, None)
            if query_result:
                plotSimilarImages(args, query_result['query_image'], query_result['similar_images'],
                                  query_result['similar_scores'], query_result['similar_locations'],
                                  query_shelf_location=query_result['shelf_location'])
    elif args.index_type == 'flat':
        result = baoli(args)
        for image_file in test_images:
            # 在调用 plotSimilarImages 的地方
            plotSimilarImages(args, image_file, result[image_file][0], result[image_file][1], result[image_file][2],
                              query_shelf_location=shelf_location.get(image_file, None))

    end_time_match = time.time()  # 记录结束时间
    print(f"Time taken to match images: {end_time_match - start_time_match:.2f} seconds")


#%%
