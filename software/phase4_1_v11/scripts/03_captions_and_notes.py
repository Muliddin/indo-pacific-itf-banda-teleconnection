from common import *
def main():
    captions = """# Final Figure Captions

**Figure 1. Validation of the native-grid Indonesian Throughflow transport framework.** (a) Section-scale transport for Lombok, Makassar, and Ombai compared with published/reference values for 2004–2006. (b) Combined Lombok–Ombai–Timor outflow compared with the 15 Sv reference. Positive transport is defined toward the Indian Ocean. Agreement is interpreted as model-framework validation rather than exact observational equivalence.

**Figure 2. Frozen ENSO and IOD teleconnections to ITF transport.** Bars show correlation coefficients at the pre-specified best positive lag retained after lag-robustness analysis. Positive lag denotes climate index leading transport. Only pathways classified as FREEZE are shown. These are associative teleconnections and not causal effects.

**Figure 3. Seasonal-year and event-level modulation of ENSO/IOD–ITF relationships.** (a,b) Seasonal-year correlations for Niño3.4 and DMI at frozen lags across DJF, MAM, JJA, and SON. (c) Event-level transport contrasts retained as FREEZE or CONDITIONAL after episode-aware bootstrap/permutation testing. Rare compound-event classes are interpreted cautiously.

**Figure 4. Coupled ITF–atmosphere–Banda Sea relationships.** (a) Conditional/canonical lagged ITF coupling with Banda Sea OHC, SST, MLD, and wind/upwelling diagnostics. (b) Mechanistic relationships classified as robust core in Phase 3B v1.1. These directionality results indicate temporal ordering and physical coherence but do not establish causation.

**Figure 5. Integrated synthesis of the climate–ITF–atmosphere–Banda Sea system.** (a) Conceptual network separating climate forcing, oceanic ITF transport, atmospheric wind/Ekman forcing, and Banda Sea heat-content response. Solid arrows denote robust climate-system associations; dashed arrows denote physically coherent but statistically non-separable mechanistic coupling. (b) Standardized direct and indirect effects from the pre-specified parallel-mediator models. Formal indirect effects through total outflow and full Ekman pumping were not robust.
"""
    notes = """# Final Table Notes

**Table 1. ITF transport validation summary.** Values are means over the stated 2004–2006 validation interval. Relative bias is reported against the adopted literature/reference transport. Model–reference agreement is used to assess framework plausibility, not to claim observational identity.

**Table 2. Core ENSO/IOD→ITF lagged relationships.** Only pathways classified as FREEZE in Phase 3A v1.1 are included. `best_positive_lag` is in months and means the climate index leads transport. Ordinary and partial correlations are reported where available; FDR-adjusted significance follows the frozen Phase 3A protocol.

**Table 3. Synthesis of seasonal/event robustness and ITF–Banda coupling.** Seasonal/event rows include only FREEZE results from Stage 2 v1.1. ITF–Banda rows include CANONICAL and CONDITIONAL relationships from Phase 3B v1.0. These categories must be preserved in interpretation; CONDITIONAL findings require explicit model/lag/season qualification.
"""
    (ROOT/"captions/Figure_Captions.md").write_text(captions,encoding="utf-8")
    (ROOT/"captions/Table_Notes.md").write_text(notes,encoding="utf-8")
    print("WROTE captions and table notes")
if __name__=="__main__":main()
