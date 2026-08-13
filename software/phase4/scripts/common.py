from pathlib import Path
import pandas as pd, numpy as np, yaml, logging, json
ROOT=Path(__file__).resolve().parents[1]
def cfg():
    with open(ROOT/'config/phase4_config.yaml') as f:return yaml.safe_load(f)
def resolve(p):
    x=Path(p).expanduser();return x if x.is_absolute() else (ROOT/x).resolve()
def log(n):
    logging.basicConfig(level=logging.INFO,format='%(asctime)s | %(levelname)s | %(name)s | %(message)s')
    return logging.getLogger(n)
