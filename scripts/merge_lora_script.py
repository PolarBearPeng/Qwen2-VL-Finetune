import torch
from transformers import Qwen2VLForConditionalGeneration, AutoProcessor
from peft import PeftModel
import argparse
from pathlib import Path

def merge_lora_weights(base_model_path, lora_path, output_path):
    """
    合并LoRA权重到基础模型
    
    Args:
        base_model_path: 基础模型路径
        lora_path: LoRA权重路径
        output_path: 输出路径
    """
    print(f"加载基础模型: {base_model_path}")
    # 加载基础模型
    model = Qwen2VLForConditionalGeneration.from_pretrained(
        base_model_path,
        torch_dtype=torch.bfloat16,
        device_map="auto",
        trust_remote_code=True
    )
    
    print(f"加载LoRA权重: {lora_path}")
    # 加载LoRA权重
    model = PeftModel.from_pretrained(
        model,
        lora_path,
        torch_dtype=torch.bfloat16
    )
    
    print("合并权重...")
    # 合并权重
    model = model.merge_and_unload()
    
    # 保存合并后的模型
    output_path = Path(output_path)
    output_path.mkdir(parents=True, exist_ok=True)
    
    print(f"保存合并后的模型到: {output_path}")
    model.save_pretrained(output_path)
    
    # 同时保存processor
    print("保存processor...")
    processor = AutoProcessor.from_pretrained(base_model_path)
    processor.save_pretrained(output_path)
    
    print("合并完成！")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="合并LoRA权重到基础模型")
    parser.add_argument("--base_model", type=str, default="Qwen/Qwen2.5-VL-7B-Instruct",
                        help="基础模型路径")
    parser.add_argument("--lora_path", type=str, required=True,
                        help="LoRA权重路径")
    parser.add_argument("--output_path", type=str, required=True,
                        help="输出路径")
    
    args = parser.parse_args()
    
    merge_lora_weights(
        base_model_path=args.base_model,
        lora_path=args.lora_path,
        output_path=args.output_path
    )