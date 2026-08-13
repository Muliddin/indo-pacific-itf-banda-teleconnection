from common import cfg,resolve,log
def main():
    c=cfg();L=log("00_preflight");r=resolve(c["inputs"]["phase3c_v10_root"])
    for p in [r/"data/processed/mediation_master_1993_2025.csv",r/"reports/primary_parallel_mediation.csv"]:
        if not p.exists():raise RuntimeError(f"Missing input: {p}")
        L.info("Input OK: %s",p)
if __name__=="__main__":main()
