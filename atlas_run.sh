#!/bin/bash
#SBATCH -A users                # Account name
#SBATCH -p mid                  # Partition (queue) name
#SBATCH --qos=users             # Quality of service
#SBATCH --gres=gpu:rtx_a6000:1       # Request 
#SBATCH -c 8                    # Reduced CPU cores to 8
#SBATCH --mem=50G               # Reduced RAM to 50GB
#SBATCH --time=1-00:00:00       # Max runtime (1 day)
#SBATCH -o results_%j.txt       # Save output to results_JOBID.txt
#SBATCH -e errors_%j.txt        # Save errors to errors_JOBID.txt
#SBATCH --mail-type=ALL
#SBATCH --mail-user=apolat21@ku.edu.tr

# Load miniconda module
module load miniconda3/4.14


# Clone the repository
git clone https://github.com/eozlu21/lm-evaluation-harness.git
cd lm-evaluation-harness


# Create and activate environment
micromamba env create -n lm_eval
micromamba activate lm_eval

# Install PyTorch with CUDA support
conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia -y

# Install other dependencies
pip install -e .
pip install transformers>=4.37.0 accelerate tiktoken einops

# Run the evaluation
bash run_lm_eval.sh
