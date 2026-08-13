from common import cfg,resolve,log
def main():
    c=cfg();L=log("00_preflight")
    p3=resolve(c["inputs"]["phase3a_v10_root"])
    pb=resolve(c["inputs"]["phase3b_v11_root"])
    for p in [
        p3/"data/processed/analysis_master_anom_detrended_1993_2025.csv",
        pb/"data/processed/full_ekman_pumping_banda_1993_2025.csv",
        pb/"reports/mechanistic_pathway_registry.csv"
    ]:
        if not p.exists():raise RuntimeError(f"Missing input: {p}")
        L.info("Input OK: %s",p)
if __name__=="__main__":main()
