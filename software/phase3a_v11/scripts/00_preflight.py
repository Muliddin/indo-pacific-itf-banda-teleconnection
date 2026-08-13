from common import cfg,resolve,log
def main():
    c=cfg(); L=log("00_preflight")
    p=resolve(c["inputs"]["phase3a_v10_root"])
    required=[
        p/"data/processed/analysis_master_anom_detrended_1993_2025.csv",
        p/"reports/lagged_ENSO_IOD_to_ITF.csv",
    ]
    for x in required:
        if not x.exists(): raise RuntimeError(f"Missing input: {x}")
        L.info("Input OK: %s",x)
    L.info("Phase 3A v1.1 preflight complete")
if __name__=="__main__":main()
