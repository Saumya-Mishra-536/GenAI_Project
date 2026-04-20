#!/usr/bin/env python3
"""
Download model files from cloud storage during deployment.
Run this script during the build process on Render.
"""

import os
import sys
from pathlib import Path

def download_models():
    """Download model files from cloud storage."""
    models_dir = Path(__file__).parent / 'models'
    models_dir.mkdir(exist_ok=True)
    
    # Option 1: Models are included locally (development)
    if (Path(__file__).parent.parent.parent / 'models').exists():
        import shutil
        source = Path(__file__).parent.parent.parent / 'models'
        for file in source.glob('*.pkl'):
            dest = models_dir / file.name
            if not dest.exists():
                print(f"Copying {file.name} to {models_dir}")
                shutil.copy2(file, dest)
        return True
    
    # Option 2: Download from cloud storage (e.g., S3, Google Cloud Storage)
    # Uncomment and configure based on your cloud provider
    """
    import boto3
    
    s3 = boto3.client('s3')
    bucket = os.getenv('MODEL_BUCKET')
    
    models = ['ev_demand_timeseries.pkl', 'scaler.pkl']
    for model in models:
        dest = models_dir / model
        if not dest.exists():
            print(f"Downloading {model} from S3...")
            s3.download_file(bucket, f'models/{model}', str(dest))
    """
    
    # Option 3: Use Hugging Face Model Hub
    # Uncomment if you host models on Hugging Face
    """
    from huggingface_hub import hf_hub_download
    
    repo_id = "your-username/your-repo"
    for file in ['ev_demand_timeseries.pkl', 'scaler.pkl']:
        dest = models_dir / file
        if not dest.exists():
            print(f"Downloading {file} from Hugging Face...")
            hf_hub_download(repo_id=repo_id, filename=file, local_dir=str(models_dir))
    """
    
    print("Model download skipped (running in development mode)")
    return True

if __name__ == '__main__':
    try:
        download_models()
        print("✓ Models ready")
        sys.exit(0)
    except Exception as e:
        print(f"✗ Error downloading models: {e}", file=sys.stderr)
        sys.exit(1)
