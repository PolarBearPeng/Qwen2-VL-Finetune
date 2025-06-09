import os
import json
from PIL import Image
from pathlib import Path
import shutil
from tqdm import tqdm

class ImagePreprocessor:
    def __init__(self, source_dir, output_dir, target_size=(1920, 1080)):
        """
        初始化图片预处理器
        
        Args:
            source_dir: 原始图片目录（包含按建筑名分类的子文件夹）
            output_dir: 输出目录
            target_size: 目标尺寸 (width, height)
        """
        self.source_dir = Path(source_dir)
        self.output_dir = Path(output_dir)
        self.images_dir = self.output_dir / "images"
        self.target_size = target_size
        
        # 创建输出目录
        self.images_dir.mkdir(parents=True, exist_ok=True)
        
        # 图片映射信息
        self.image_info = {}
        
    def resize_image(self, image_path, output_path):
        """
        调整图片大小，保持宽高比
        """
        try:
            img = Image.open(image_path)
            
            # 转换为RGB（如果是RGBA或其他格式）
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # 计算缩放比例，保持宽高比
            img_ratio = img.width / img.height
            target_ratio = self.target_size[0] / self.target_size[1]
            
            if img_ratio > target_ratio:
                # 图片更宽，以宽度为准
                new_width = self.target_size[0]
                new_height = int(new_width / img_ratio)
            else:
                # 图片更高，以高度为准
                new_height = self.target_size[1]
                new_width = int(new_height * img_ratio)
            
            # 调整大小
            img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # 创建目标尺寸的画布（可选，如果需要固定尺寸）
            # canvas = Image.new('RGB', self.target_size, (255, 255, 255))
            # paste_x = (self.target_size[0] - new_width) // 2
            # paste_y = (self.target_size[1] - new_height) // 2
            # canvas.paste(img_resized, (paste_x, paste_y))
            # canvas.save(output_path, quality=95)
            
            # 直接保存调整后的图片
            img_resized.save(output_path, quality=95)
            
            return True
        except Exception as e:
            print(f"处理图片 {image_path} 时出错: {e}")
            return False
    
    def process_all_images(self):
        """
        处理所有图片
        """
        image_counter = 0
        
        # 遍历所有建筑文件夹
        for building_dir in self.source_dir.iterdir():
            if not building_dir.is_dir():
                continue
                
            building_name = building_dir.name
            print(f"\n处理建筑: {building_name}")
            
            # 该建筑的图片列表
            building_images = []
            
            # 遍历该建筑的所有图片
            image_files = list(building_dir.glob("*.jpg")) + list(building_dir.glob("*.JPG")) + \
                         list(building_dir.glob("*.png")) + list(building_dir.glob("*.PNG"))
            
            for img_path in tqdm(image_files, desc=f"处理 {building_name} 的图片"):
                # 生成新的文件名
                new_filename = f"hku_{building_name}_{image_counter:06d}.jpg"
                output_path = self.images_dir / new_filename
                
                # 处理图片
                if self.resize_image(img_path, output_path):
                    building_images.append({
                        "original_name": img_path.name,
                        "new_name": new_filename,
                        "building": building_name,
                        "original_path": str(img_path),
                        "processed_path": str(output_path)
                    })
                    image_counter += 1
            
            # 保存该建筑的图片信息
            self.image_info[building_name] = building_images
        
        # 保存映射信息
        info_path = self.output_dir / "image_info.json"
        with open(info_path, 'w', encoding='utf-8') as f:
            json.dump(self.image_info, f, ensure_ascii=False, indent=2)
        
        print(f"\n处理完成！共处理 {image_counter} 张图片")
        print(f"图片信息保存在: {info_path}")
        
        return self.image_info

# 使用示例
if __name__ == "__main__":
    # 设置路径
    source_directory = "/path/to/your/original/images"  # 包含建筑文件夹的目录
    output_directory = "/path/to/processed/dataset"
    
    # 创建预处理器并处理图片
    preprocessor = ImagePreprocessor(
        source_dir=source_directory,
        output_dir=output_directory,
        target_size=(1920, 1080)  # 可以根据需要调整
    )
    
    # 处理所有图片
    image_info = preprocessor.process_all_images()
    
    # 打印统计信息
    print("\n各建筑图片统计:")
    for building, images in image_info.items():
        print(f"{building}: {len(images)} 张图片")