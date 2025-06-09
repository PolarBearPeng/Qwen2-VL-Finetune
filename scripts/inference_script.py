import torch
from transformers import Qwen2VLForConditionalGeneration, AutoProcessor
from qwen_vl_utils import process_vision_info
from PIL import Image
import argparse
from pathlib import Path

class HKUCampusGuide:
    def __init__(self, model_path, device="cuda"):
        """
        初始化HKU校园导览模型
        
        Args:
            model_path: 合并后的模型路径
            device: 运行设备
        """
        self.device = device
        
        # 加载模型和处理器
        print(f"加载模型: {model_path}")
        self.model = Qwen2VLForConditionalGeneration.from_pretrained(
            model_path,
            torch_dtype=torch.bfloat16,
            device_map="auto"
        ).eval()
        
        self.processor = AutoProcessor.from_pretrained(model_path)
        
    def chat(self, image_path, question, language="auto"):
        """
        与模型对话
        
        Args:
            image_path: 图片路径
            question: 用户问题
            language: 语言设置 ("auto", "en", "zh")
        """
        # 检测语言（简单实现）
        if language == "auto":
            # 检查是否包含中文字符
            if any('\u4e00' <= char <= '\u9fff' for char in question):
                detected_language = "zh"
            else:
                detected_language = "en"
        else:
            detected_language = language
        
        # 构建消息
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "image": image_path,
                    },
                    {
                        "type": "text",
                        "text": question
                    }
                ]
            }
        ]
        
        # 准备输入
        text = self.processor.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
        
        image_inputs, video_inputs = process_vision_info(messages)
        inputs = self.processor(
            text=[text],
            images=image_inputs,
            videos=video_inputs,
            padding=True,
            return_tensors="pt"
        ).to(self.device)
        
        # 生成回答
        with torch.no_grad():
            generated_ids = self.model.generate(
                **inputs,
                max_new_tokens=512,
                temperature=0.7,
                top_p=0.9,
                do_sample=True
            )
        
        # 解码输出
        generated_ids_trimmed = [
            out_ids[len(in_ids):] for in_ids, out_ids in zip(inputs.input_ids, generated_ids)
        ]
        response = self.processor.batch_decode(
            generated_ids_trimmed, 
            skip_special_tokens=True, 
            clean_up_tokenization_spaces=False
        )[0]
        
        return response
    
    def interactive_demo(self):
        """
        交互式演示
        """
        print("\n=== HKU Campus Building Guide ===")
        print("香港大学校园建筑导览助手\n")
        print("Instructions:")
        print("1. Enter the path to a building image")
        print("2. Ask questions about the building")
        print("3. Type 'quit' to exit\n")
        
        while True:
            # 获取图片路径
            image_path = input("Image path (or 'quit' to exit): ").strip()
            if image_path.lower() == 'quit':
                break
            
            # 检查图片是否存在
            if not Path(image_path).exists():
                print(f"Error: Image not found at {image_path}")
                continue
            
            # 持续对话
            print("\nYou can now ask questions about this building. Type 'next' for a new image.\n")
            while True:
                question = input("Your question: ").strip()
                if question.lower() == 'next':
                    break
                if not question:
                    continue
                
                # 获取回答
                print("\nThinking...")
                response = self.chat(image_path, question)
                print(f"\nAssistant: {response}\n")

def main():
    parser = argparse.ArgumentParser(description="HKU校园建筑导览推理")
    parser.add_argument("--model_path", type=str, required=True,
                        help="合并后的模型路径")
    parser.add_argument("--image", type=str, help="测试图片路径")
    parser.add_argument("--question", type=str, help="测试问题")
    parser.add_argument("--interactive", action="store_true",
                        help="启动交互式模式")
    
    args = parser.parse_args()
    
    # 初始化模型
    guide = HKUCampusGuide(args.model_path)
    
    if args.interactive:
        # 交互式模式
        guide.interactive_demo()
    elif args.image and args.question:
        # 单次测试
        response = guide.chat(args.image, args.question)
        print(f"Question: {args.question}")
        print(f"Answer: {response}")
    else:
        print("请提供 --interactive 参数或同时提供 --image 和 --question 参数")

if __name__ == "__main__":
    main()