#!/bin/bash
#SBATCH -A users                # Account name
#SBATCH -p mid                  # Partition (queue) name
#SBATCH --qos=users             # Quality of service
#SBATCH --gres=gpu:a100:1       # Request 1 A100 GPU
#SBATCH -c 8                    # Reduced CPU cores to 8
#SBATCH --mem=100G              # Reduced RAM to 100GB
#SBATCH --time=1-00:00:00       # Max runtime (1 day)
#SBATCH -o results_%j.txt       # Save output to results_JOBID.txt
#SBATCH -e errors_%j.txt        # Save errors to errors_JOBID.txt
#SBATCH --mail-type=ALL
#SBATCH --mail-user=apolat21@ku.edu.tr

# Load required modules
module load cuda/12.0

# Initialize micromamba
eval "$(micromamba shell hook --shell bash)"

# Change to the evaluation directory
cd lm-evaluation-harness

# Create and activate environment (only if it doesn't exist)
micromamba env create -n lm_eval -y || true
micromamba activate lm_eval

# Install Python and dependencies
micromamba install python==3.12.9 -y
pip install -e .

# Install additional dependencies for Qwen
pip install torch>=2.0.0 transformers>=4.37.0 accelerate tiktoken einops

# Run the evaluation
bash run_lm_eval.sh