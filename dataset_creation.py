import json
import random
from pathlib import Path
from typing import List, Dict

class HKUCampusDatasetCreator:
    def __init__(self, image_info_path, output_path):
        """
        创建香港大学校园建筑数据集
        
        Args:
            image_info_path: image_info.json的路径
            output_path: 输出数据集JSON的路径
        """
        self.output_path = Path(output_path)
        
        # 加载图片信息
        with open(image_info_path, 'r', encoding='utf-8') as f:
            self.image_info = json.load(f)
        
        # 定义建筑信息（需要根据实际情况填充）
        self.building_info = {
            "main_building": {
                "en_name": "Main Building",
                "cn_name": "本部大楼",
                "description_en": "The Main Building is the oldest building of HKU, completed in 1912. It features Edwardian Baroque architecture and is a declared monument.",
                "description_cn": "本部大楼是香港大学最古老的建筑，建于1912年。它采用爱德华巴洛克建筑风格，是法定古迹。",
                "location": "Pok Fu Lam Road",
                "year_built": "1912",
                "architect": "Leigh & Orange",
                "features": ["Clock Tower", "Great Hall", "Colonial Architecture"]
            },
            "library": {
                "en_name": "Main Library",
                "cn_name": "总图书馆",
                "description_en": "The Main Library is the largest library at HKU, housing over 2.8 million volumes.",
                "description_cn": "总图书馆是香港大学最大的图书馆，藏书超过280万册。",
                "location": "Pok Fu Lam Road",
                "year_built": "1961",
                "features": ["Study rooms", "Digital resources", "Special collections"]
            },
            # 添加更多建筑信息...
        }
        
    def create_qa_pairs(self, building_name: str, image_names: List[str]) -> List[Dict]:
        """
        为特定建筑创建问答对
        """
        qa_templates = [
            # 基础识别问题
            {
                "en": [
                    {"q": "What building is shown in this image?", "a": f"This is the {self.building_info.get(building_name, {}).get('en_name', building_name)} of the University of Hong Kong."},
                    {"q": "Can you identify this HKU building?", "a": f"Yes, this is the {self.building_info.get(building_name, {}).get('en_name', building_name)}. {self.building_info.get(building_name, {}).get('description_en', '')}"},
                ],
                "cn": [
                    {"q": "这张图片展示的是什么建筑？", "a": f"这是香港大学的{self.building_info.get(building_name, {}).get('cn_name', building_name)}。"},
                    {"q": "你能识别这座港大建筑吗？", "a": f"这是{self.building_info.get(building_name, {}).get('cn_name', building_name)}。{self.building_info.get(building_name, {}).get('description_cn', '')}"},
                ]
            },
            # 历史相关问题
            {
                "en": [
                    {"q": "When was this building constructed?", "a": f"The {self.building_info.get(building_name, {}).get('en_name', building_name)} was built in {self.building_info.get(building_name, {}).get('year_built', 'unknown year')}."},
                    {"q": "Tell me about the history of this building.", "a": f"The {self.building_info.get(building_name, {}).get('en_name', building_name)} was constructed in {self.building_info.get(building_name, {}).get('year_built', 'unknown year')}. {self.building_info.get(building_name, {}).get('description_en', '')}"},
                ],
                "cn": [
                    {"q": "这座建筑是什么时候建造的？", "a": f"{self.building_info.get(building_name, {}).get('cn_name', building_name)}建于{self.building_info.get(building_name, {}).get('year_built', '未知年份')}年。"},
                    {"q": "介绍一下这座建筑的历史。", "a": f"{self.building_info.get(building_name, {}).get('cn_name', building_name)}建于{self.building_info.get(building_name, {}).get('year_built', '未知年份')}年。{self.building_info.get(building_name, {}).get('description_cn', '')}"},
                ]
            },
            # 位置相关问题
            {
                "en": [
                    {"q": "Where is this building located on campus?", "a": f"The {self.building_info.get(building_name, {}).get('en_name', building_name)} is located at {self.building_info.get(building_name, {}).get('location', 'HKU campus')}."},
                    {"q": "How can I find this building?", "a": f"This is the {self.building_info.get(building_name, {}).get('en_name', building_name)}, located at {self.building_info.get(building_name, {}).get('location', 'HKU campus')}. You can access it from the main entrance."},
                ],
                "cn": [
                    {"q": "这座建筑在校园的什么位置？", "a": f"{self.building_info.get(building_name, {}).get('cn_name', building_name)}位于{self.building_info.get(building_name, {}).get('location', '港大校园')}。"},
                    {"q": "如何找到这座建筑？", "a": f"这是{self.building_info.get(building_name, {}).get('cn_name', building_name)}，位于{self.building_info.get(building_name, {}).get('location', '港大校园')}。您可以从主入口进入。"},
                ]
            },
            # 功能相关问题
            {
                "en": [
                    {"q": "What is the function of this building?", "a": f"The {self.building_info.get(building_name, {}).get('en_name', building_name)} serves as {self.building_info.get(building_name, {}).get('description_en', 'an important facility at HKU')}."},
                    {"q": "What facilities are available in this building?", "a": f"The {self.building_info.get(building_name, {}).get('en_name', building_name)} features {', '.join(self.building_info.get(building_name, {}).get('features', ['various facilities']))}."},
                ],
                "cn": [
                    {"q": "这座建筑的功能是什么？", "a": f"{self.building_info.get(building_name, {}).get('cn_name', building_name)}{self.building_info.get(building_name, {}).get('description_cn', '是港大的重要设施')}。"},
                    {"q": "这座建筑里有什么设施？", "a": f"{self.building_info.get(building_name, {}).get('cn_name', building_name)}内设有{', '.join(self.building_info.get(building_name, {}).get('features', ['各种设施']))}。"},
                ]
            }
        ]
        
        return qa_templates
    
    def create_conversations(self, qa_pair: Dict, language: str) -> List[Dict]:
        """
        创建对话格式
        """
        conversations = []
        conversations.append({
            "from": "human",
            "value": f"<image>\n{qa_pair['q']}"
        })
        conversations.append({
            "from": "gpt",
            "value": qa_pair['a']
        })
        return conversations
    
    def create_dataset(self):
        """
        创建完整的数据集
        """
        dataset = []
        sample_id = 0
        
        for building_name, images in self.image_info.items():
            print(f"处理建筑: {building_name}")
            
            # 获取该建筑的问答模板
            qa_templates = self.create_qa_pairs(building_name, [img['new_name'] for img in images])
            
            # 为每张图片创建多个问答对
            for img_info in images:
                # 英文问答
                for qa_group in qa_templates:
                    for qa in qa_group['en']:
                        dataset.append({
                            "id": f"hku_{sample_id:06d}",
                            "image": img_info['new_name'],
                            "conversations": self.create_conversations(qa, 'en')
                        })
                        sample_id += 1
                
                # 中文问答
                for qa_group in qa_templates:
                    for qa in qa_group['cn']:
                        dataset.append({
                            "id": f"hku_{sample_id:06d}",
                            "image": img_info['new_name'],
                            "conversations": self.create_conversations(qa, 'cn')
                        })
                        sample_id += 1
        
        # 添加多轮对话示例
        dataset.extend(self.create_multi_turn_examples())
        
        # 随机打乱数据
        random.shuffle(dataset)
        
        # 划分训练集和验证集
        split_point = int(len(dataset) * 0.9)
        train_data = dataset[:split_point]
        val_data = dataset[split_point:]
        
        # 保存数据集
        train_path = self.output_path.parent / f"{self.output_path.stem}_train.json"
        val_path = self.output_path.parent / f"{self.output_path.stem}_val.json"
        
        with open(train_path, 'w', encoding='utf-8') as f:
            json.dump(train_data, f, ensure_ascii=False, indent=2)
        
        with open(val_path, 'w', encoding='utf-8') as f:
            json.dump(val_data, f, ensure_ascii=False, indent=2)
        
        print(f"\n数据集创建完成！")
        print(f"训练集: {len(train_data)} 个样本 - {train_path}")
        print(f"验证集: {len(val_data)} 个样本 - {val_path}")
        
        return train_data, val_data
    
    def create_multi_turn_examples(self) -> List[Dict]:
        """
        创建多轮对话示例
        """
        multi_turn_examples = [
            {
                "id": "hku_multi_001",
                "image": "hku_main_building_000001.jpg",  # 需要替换为实际的图片名
                "conversations": [
                    {"from": "human", "value": "<image>\nWhat building is this?"},
                    {"from": "gpt", "value": "This is the Main Building of the University of Hong Kong, the oldest building on campus."},
                    {"from": "human", "value": "When was it built?"},
                    {"from": "gpt", "value": "The Main Building was completed in 1912, making it over 110 years old."},
                    {"from": "human", "value": "What architectural style does it represent?"},
                    {"from": "gpt", "value": "The Main Building features Edwardian Baroque architecture, which was popular in the early 20th century. It combines classical elements with ornate decorative features, including the distinctive clock tower."}
                ]
            },
            {
                "id": "hku_multi_002",
                "image": "hku_library_000001.jpg",  # 需要替换为实际的图片名
                "conversations": [
                    {"from": "human", "value": "<image>\n这是什么地方？"},
                    {"from": "gpt", "value": "这是香港大学总图书馆，是港大最大的图书馆。"},
                    {"from": "human", "value": "图书馆有多少藏书？"},
                    {"from": "gpt", "value": "总图书馆藏书超过280万册，是香港最大的学术图书馆之一。"},
                    {"from": "human", "value": "开放时间是什么时候？"},
                    {"from": "gpt", "value": "图书馆在学期期间通常从早上8点开放至晚上11点，周末和假期的开放时间会有所调整。建议查看图书馆官网获取最新的开放时间信息。"}
                ]
            }
        ]
        
        return multi_turn_examples

# 使用示例
if __name__ == "__main__":
    # 创建数据集
    creator = HKUCampusDatasetCreator(
        image_info_path="/path/to/processed/dataset/image_info.json",
        output_path="/path/to/processed/dataset/hku_campus_dataset.json"
    )
    
    # 生成数据集
    train_data, val_data = creator.create_dataset()