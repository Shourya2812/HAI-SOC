"""
Central configuration for the ML pipeline.
"""

from pathlib import Path

# Project Root
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Dataset Paths
DATASET_DIR = PROJECT_ROOT / "datasets" / "processed"

ML_DATASET = DATASET_DIR / "ml_dataset.csv"

# Random Seed
RANDOM_STATE = 42

# Train/Test Split
TEST_SIZE = 0.20