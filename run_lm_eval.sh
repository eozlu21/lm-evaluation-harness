#!/bin/bash

lm_eval --model hf \
        --model_args pretrained=microsoft/phi-2,dtype=float32 \
        --tasks yks_tyt_2024 \
        --num_fewshot 0 \
        --log_samples \
        --output_path logs/ \
        --device cuda:0 \