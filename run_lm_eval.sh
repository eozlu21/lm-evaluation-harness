#!/bin/bash

lm_eval --model hf \
        --model_args pretrained=Qwen/Qwen3-8B-Instruct,dtype=float32,thinking_mode=True \
        --tasks yks_2024 \
        --num_fewshot 5 \
        --log_samples \
        --output_path atlas_logs/ \
        --device cuda:0