from pathlib import Path
import importlib, platform, sys
from common import cfg,phase2b_root,log
def main():
    c=cfg(); L=log("00_preflight")
    L.info("Platform: %s",platform.platform()); L.info("Python: %s",sys.version.split()[0])
    for m in ["xarray","netCDF4","numpy","pandas","yaml","dask","scipy"]:
        mod=importlib.import_module(m); L.info("Dependency OK %s %s",m,getattr(mod,"__version__","unknown"))
    p2b=phase2b_root(c)
    if not p2b.exists(): raise RuntimeError(f"Phase 2B root not found: {p2b}")
    required=[p2b/"data/raw/glorys",p2b/"data/raw/era5",p2b/"data/raw/duacs",
              p2b/"data/raw/noaa_indices/nino34_canonical.csv",
              p2b/"data/raw/noaa_indices/dmi_canonical.csv"]
    for p in required:
        if not p.exists(): raise RuntimeError(f"Missing Phase 2B input: {p}")
        L.info("Input OK: %s",p)
    L.info("Phase 2C preflight complete.")
if __name__=="__main__": main()
