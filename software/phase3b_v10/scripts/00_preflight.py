from common import cfg,resolve,log
def main():
    c=cfg();L=log("00_preflight")
    p3=resolve(c["inputs"]["phase3a_v10_root"])
    s2=resolve(c["inputs"]["phase3a_stage2_v11_root"])
    req=[
        p3/"data/processed/analysis_master_anom_detrended_1993_2025.csv",
        s2/"reports/stage2_freeze_decision.csv",
    ]
    for p in req:
        if not p.exists():
            raise RuntimeError(f"Missing input: {p}")
        L.info("Input OK: %s",p)
if __name__=="__main__":
    main()
