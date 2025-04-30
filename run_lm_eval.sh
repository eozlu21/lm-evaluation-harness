#!/bin/bash

lm_eval --model hf \
        --model_args pretrained=mistralai/Mistral-Small-3.1-24B-Instruct-2503,dtype=float32 \
        --tasks yks_tyt_2024 \
        --num_fewshot 0 \
        --log_samples \
        --output_path logs/ \
        --device cuda:0