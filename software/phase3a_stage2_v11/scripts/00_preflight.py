from common import cfg,resolve,log
def main():
    c=cfg();L=log("00_preflight")
    p10=resolve(c["inputs"]["phase3a_v10_root"])
    s20=resolve(c["inputs"]["stage2_v10_root"])
    req=[
        p10/"data/processed/analysis_master_anom_detrended_1993_2025.csv",
        s20/"data/processed/event_classification_1993_2025.csv",
        s20/"reports/seasonal_stratified_frozen_lags.csv"
    ]
    for p in req:
        if not p.exists():
            raise RuntimeError(f"Missing input: {p}")
        L.info("Input OK: %s",p)
if __name__=="__main__":
    main()
