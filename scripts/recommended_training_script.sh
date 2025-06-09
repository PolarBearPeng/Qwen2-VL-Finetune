#!/bin/bash

# 推荐方案：LLM LoRA + Vision Full Training
# 这个方案最适合学习新的视觉概念（HKU建筑）

MODEL_NAME="Qwen/Qwen2.5-VL-7B-Instruct"

export PYTHONPATH=src:$PYTHONPATH

# 批次设置
GLOBAL_BATCH_SIZE=64
BATCH_PER_DEVICE=2    # 根据显存调整
NUM_DEVICES=8
GRAD_ACCUM_STEPS=$((GLOBAL_BATCH_SIZE / (BATCH_PER_DEVICE * NUM_DEVICES)))

# 数据路径
DATA_PATH="/path/to/processed/dataset/hku_campus_dataset_train.json"
VAL_DATA_PATH="/path/to/processed/dataset/hku_campus_dataset_val.json"
IMAGE_FOLDER="/path/to/processed/dataset/images"

OUTPUT_DIR="output/hku_campus_llm_lora_vision_full_$(date +%Y%m%d_%H%M%S)"

# 训练命令
deepspeed src/train/train_sft.py \
    --use_liger True \
    --lora_enable True \
    --vision_lora False \
    --use_dora False \
    --lora_namespan_exclude "['lm_head', 'embed_tokens', 'vision_model', 'merger']" \
    --lora_rank 128 \
    --lora_alpha 256 \
    --lora_dropout 0.05 \
    --num_lora_modules -1 \
    --deepspeed scripts/zero2.json \
    --model_id $MODEL_NAME \
    --data_path $DATA_PATH \
    --eval_data_path $VAL_DATA_PATH \
    --image_folder $IMAGE_FOLDER \
    --remove_unused_columns False \
    --freeze_vision_tower False \
    --freeze_llm True \
    --freeze_merger False \
    --bf16 True \
    --fp16 False \
    --disable_flash_attn2 False \
    --output_dir $OUTPUT_DIR \
    --num_train_epochs 5 \
    --per_device_train_batch_size $BATCH_PER_DEVICE \
    --per_device_eval_batch_size $BATCH_PER_DEVICE \
    --gradient_accumulation_steps $GRAD_ACCUM_STEPS \
    --image_min_pixels $((448 * 28 * 28)) \
    --image_max_pixels $((896 * 28 * 28)) \
    --learning_rate 1e-4 \
    --merger_lr 2e-5 \
    --vision_lr 2e-6 \
    --weight_decay 0.05 \
    --warmup_ratio 0.1 \
    --lr_scheduler_type "cosine" \
    --logging_steps 10 \
    --eval_strategy "steps" \
    --eval_steps 50 \
    --save_strategy "steps" \
    --save_steps 100 \
    --save_total_limit 3 \
    --load_best_model_at_end True \
    --metric_for_best_model "eval_loss" \
    --greater_is_better False \
    --tf32 True \
    --gradient_checkpointing True \
    --report_to tensorboard \
    --lazy_preprocess True \
    --dataloader_num_workers 4 \
    --max_seq_length 2048 \
    --run_name "hku_llm_lora_vision_full"

echo "训练完成！模型保存在: $OUTPUT_DIR"

# 训练完成后的提示
echo "
下一步：
1. 查看训练日志: tensorboard --logdir=$OUTPUT_DIR
2. 合并LoRA权重: python merge_lora.py --lora_path $OUTPUT_DIR/checkpoint-best
3. 测试模型效果: python inference.py --model_path <merged_model_path> --interactive
"