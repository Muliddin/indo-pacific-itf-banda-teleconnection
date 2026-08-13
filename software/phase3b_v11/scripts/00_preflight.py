from common import cfg,resolve,find_era5_gridded,log
def main():
    c=cfg();L=log("00_preflight")
    p2=resolve(c["inputs"]["phase2c_root"])
    p3=resolve(c["inputs"]["phase3a_v10_root"])
    p3b=resolve(c["inputs"]["phase3b_v10_root"])
    for p in [p3/"data/processed/analysis_master_anom_detrended_1993_2025.csv",
              p3b/"reports/canonical_ITF_Banda_coupling.csv"]:
        if not p.exists():raise RuntimeError(f"Missing input: {p}")
        L.info("Input OK: %s",p)
    era=find_era5_gridded(p2,c["variables"]["era5_tau_x"],c["variables"]["era5_tau_y"])
    L.info("ERA5 gridded source: %s",era)
if __name__=="__main__":main()
