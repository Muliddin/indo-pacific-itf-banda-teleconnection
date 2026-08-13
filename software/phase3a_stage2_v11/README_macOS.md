# Phase3A_Stage2_v1.1_EventAware_SeasonalRobustness

Publication-grade robustness gate before ITF→OHC/upwelling coupling.

## Improvements over Stage 2 v1.0
- seasonal inference uses one mean per season-year;
- event composites use independent persistent episodes;
- bootstrap and permutation operate on episode means;
- compound event classes get sample-size flags;
- automatic FREEZE / CONDITIONAL / REVIEW decisions are produced.

## Run
```bash
cd ~/Downloads/Phase3A_Stage2_v1.1_EventAware_SeasonalRobustness
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
bash run_stage2_v1.1.sh
```

## Main outputs
- reports/seasonal_year_correlations.csv
- data/processed/event_episode_registry.csv
- reports/event_episode_counts.csv
- reports/event_level_composites.csv
- reports/compound_event_robustness.csv
- figures/seasonal_year_heatmap_nino34.png
- figures/seasonal_year_heatmap_dmi.png
- reports/stage2_freeze_decision.csv
- reports/stage2_v11_summary.json

## Freeze rules
Seasonal-year:
- FREEZE if global FDR passes and |r| >= 0.30
- CONDITIONAL if only one condition passes
- REVIEW otherwise

Event composites:
- FREEZE if FDR passes and both groups have >=5 independent episodes
- CONDITIONAL if FDR passes and both groups have >=3 episodes
- REVIEW otherwise

Mediation remains deferred until this stage is reviewed.
