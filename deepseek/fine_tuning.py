from unsloth import FastLanguageModel
import os
import logging
from datasets import load_dataset
from transformers import BitsAndBytesConfig
from trl import SFTTrainer, SFTConfig

# 设置基础模型和缓存路径
model_name = "unsloth/Qwen3-32B-bnb-4bit"
cache_dir = "/root/autodl-tmp/llm-model"

# 1. 加载底座量化模型
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype="float16",
)

base_model, tokenizer = FastLanguageModel.from_pretrained(
    model_name=model_name,
    cache_dir=cache_dir,
    max_seq_length=4096,
    load_in_4bit=True,
)

# 2. 通用训练函数（支持 CNN/DailyMail 和 MeetingBank）
def train_stage(
    base_model,
    tokenizer,
    dataset_name,
    train_split,
    val_split,
    preprocess_fn,
    adapter_save_path,
    output_dir,
    max_steps,
    learning_rate,
    stage_name="stage",
    name=None
):
    if os.path.exists(adapter_save_path):
        print(f"✅ {stage_name} 已存在，跳过训练。")
        return

    print(f"🚀 开始微调：{stage_name}")

    # 加载 & 预处理数据
    raw_train = load_dataset(dataset_name, name, split=train_split, cache_dir=cache_dir)
    raw_val = load_dataset(dataset_name, name, split=val_split, cache_dir=cache_dir)

    train_dataset = raw_train.map(preprocess_fn, batched=True, remove_columns=raw_train.column_names)
    val_dataset = raw_val.map(preprocess_fn, batched=True, remove_columns=raw_val.column_names)

    # 初始化 LoRA
    model = FastLanguageModel.get_peft_model(
        base_model,
        r=32,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
        lora_alpha=32,
        lora_dropout=0,
        bias="none",
        use_gradient_checkpointing="unsloth",
        random_state=3407,
        use_rslora=False,
        loftq_config=None,
    )

    training_args = SFTConfig(
        output_dir=output_dir,
        dataset_text_field="text",
        per_device_train_batch_size=2,
        gradient_accumulation_steps=4,
        warmup_steps=5,
        max_steps=max_steps,
        learning_rate=learning_rate,
        logging_steps=1,
        optim="adamw_8bit",
        weight_decay=0.01,
        lr_scheduler_type="linear",
        seed=3407,
        report_to="none",
    )

    trainer = SFTTrainer(
        model=model,
        tokenizer=tokenizer,
        train_dataset=train_dataset,
        eval_dataset=val_dataset,
        dataset_text_field="text",
        dataset_label_field="summary",
        args=training_args,
    )

    trainer.train()
    print(f"✅ {stage_name} 训练完成")
    trainer.model.save_pretrained(adapter_save_path)
    tokenizer.save_pretrained(adapter_save_path)

# 3. CNN/DailyMail 微调阶段
train_stage(
    base_model=base_model,
    tokenizer=tokenizer,
    dataset_name="cnn_dailymail",
    train_split="train",
    val_split="validation",
    preprocess_fn=lambda batch: {
        "text": [f"<|user|>\nPlease summarize the following article:\n\n{doc}\n<|end|>" for doc in batch["article"]],
        "summary": batch["highlights"]
    },
    adapter_save_path=f"{cache_dir}/qwen3-32b-summarization-lora-finetuned",
    output_dir=f"{cache_dir}/qwen3-32b-summarization-lora",
    max_steps=30,
    learning_rate=2e-4,
    stage_name="CNN/DailyMail 微调",
    name="3.0.0",
)

# 4. MeetingBank 微调阶段
train_stage(
    base_model=base_model,
    tokenizer=tokenizer,
    dataset_name="huuuyeah/meetingbank",
    train_split="train",
    val_split="validation",
    preprocess_fn=lambda batch: {
        "text": [f"<|user|>\nSummarize this meeting transcript:\n\n{transcript}\n<|end|>" for transcript in batch["transcript"]],
        "summary": batch["summary"]
    },
    adapter_save_path=f"{cache_dir}/qwen3-32b-summarization-lora-finetuned-meetingbank",
    output_dir=f"{cache_dir}/qwen3-32b-summarization-lora-meetingbank",
    max_steps=30,
    learning_rate=2e-5,
    stage_name="MeetingBank 微调"
)
