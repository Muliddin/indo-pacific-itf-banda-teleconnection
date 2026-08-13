from common import *
def main():
 c=cfg()
 v=pd.read_csv(ROOT/'tables/Table_1_total_outflow_validation.csv').iloc[0]
 lag=pd.read_csv(ROOT/'tables/Table_2_ENSO_IOD_ITF_lagged.csv')
 seas=pd.read_csv(ROOT/'tables/Table_3_seasonal_event_robustness.csv')
 coup=pd.read_csv(ROOT/'tables/Table_4_ITF_Banda_coupling.csv')
 med=pd.read_csv(ROOT/'tables/Table_5_parallel_mediation.csv')
 com=pd.read_csv(ROOT/'tables/Table_S2_commonality.csv')
 robust=lag[lag.freeze_status=='FREEZE'] if 'freeze_status' in lag else lag
 son=seas[(seas.get('season',pd.Series(index=seas.index,dtype=str)).astype(str)=='SON') & (seas.get('freeze_status',pd.Series(index=seas.index,dtype=str))=='FREEZE')]
 txt=f"""# Results

## 1. Validation of the Indonesian Throughflow transport framework

The native-grid section framework reproduced the large-scale magnitude of Indonesian Throughflow outflow while retaining explicit section-level uncertainty. For the 2004–2006 validation interval, the combined Lombok–Ombai–Timor outflow was {v['model_total_outflow_2004_2006_sv']:.2f} Sv compared with the {v['instant_reference_sv']:.2f} Sv reference, corresponding to a relative bias of {v['relative_bias_percent']:.2f}%. This agreement supports use of the frozen native-grid transports for subsequent teleconnection analysis, while individual section biases are retained as methodological uncertainty rather than treated as exact observational equivalence.

## 2. ENSO and IOD teleconnections to ITF transport

Lag-robustness analysis identified {len(robust)} frozen climate–transport relationships. Niño3.4 showed predominantly negative associations with the major outflow sections and total outflow, consistent with reduced ITF transport during positive ENSO conditions. The strongest frozen total-outflow association occurred at or near zero lag, whereas Makassar and Lombok displayed section-specific lag structure. DMI effects were less spatially uniform: robust relationships were retained for Lombok, Ombai, Timor, and total outflow, while the DMI–Makassar relationship remained under review. These results indicate that ENSO/IOD forcing is expressed heterogeneously across the ITF pathway rather than as a spatially uniform transport response.

## 3. Seasonal and event dependence

Seasonal-year and independent-event analyses demonstrated marked phase locking. SON contained {len(son)} frozen seasonal relationships, with particularly strong negative ENSO/IOD associations for Ombai, Timor, and total outflow. Event-level contrasts provided additional support for ENSO-related transport changes, but compound IOD/ENSO contrasts were more sample-limited and are therefore interpreted conditionally. This distinction is important because monthly significance alone would overstate evidence from rare compound-event classes.

## 4. ITF and atmospheric coupling with Banda Sea variability

Lagged ITF–Banda analysis showed coherent associations between transport and upper-ocean variability. Total outflow was positively associated with OHC300 and OHC700 at short positive lags, while transport was also related to wind-stress curl and Ekman-pumping diagnostics. After adjustment for Niño3.4 and DMI, however, most transport–OHC relationships weakened and were classified as conditional rather than canonical. This attenuation indicates that a substantial fraction of the apparent ITF–Banda covariance is shared with basin-scale climate forcing.

Full Ekman pumping and wind stress exhibited strong associations with Banda Sea thermodynamic variability. Directionality tests favored atmospheric forcing preceding several ITF responses, while some transport–Ekman relationships were bidirectional or consistent with common forcing. These tests are interpreted as temporal-directionality evidence and not as proof of causation.

## 5. Parallel and single-mediator path analysis

Formal mediation did not identify robust indirect pathways from Niño3.4 or DMI to OHC300/OHC700 through either total ITF outflow or full Ekman pumping. All eight single-mediator diagnostics were classified as no robust mediation, consistent with the parallel-mediator analysis. Qout and full Ekman were only weakly correlated (r≈0.223; VIF≈1.05), excluding substantial mediator multicollinearity as the explanation for the null indirect effects.

Commonality analysis further showed that climate indices alone explained approximately {com.r2_base_climate.min()*100:.1f}–{com.r2_base_climate.max()*100:.1f}% of OHC variance in the fitted models, whereas adding Qout and Ekman increased explained variance by less than one percentage point. Shared Qout–Ekman variance was very small. Thus, failure to detect mediation cannot be attributed to strong collinearity or suppression; rather, the direct/shared climate signal dominates monthly OHC variability in this statistical framework.

# Discussion

## 1. A seasonally structured climate–ITF–Banda Sea system

The results support a coupled rather than strictly sequential interpretation of the ENSO/IOD–ITF–Banda Sea system. ENSO and IOD are robustly associated with ITF transport, and these relationships are strongly season dependent. At the same time, ITF transport, wind forcing, Ekman pumping, and Banda Sea heat content covary on monthly-to-seasonal timescales. The combined evidence therefore supports physical connectivity among these components without requiring a simple causal chain in which climate variability acts exclusively through ITF transport.

The particularly strong SON relationships are physically consistent with the seasonal development of Indo-Pacific climate modes and regional monsoon/ocean circulation. However, the present analysis establishes statistical phase locking rather than a unique dynamical mechanism. Rare compound events should be treated especially cautiously because event-level sample sizes are substantially smaller than the monthly record.

## 2. Why strong coupling does not imply statistically identifiable mediation

A central result is the contrast between strong pairwise teleconnections and weak formal indirect effects. This is not contradictory. Mediation asks whether a distinct portion of the climate–OHC relationship can be assigned to a specified intermediate variable after controlling for the climate driver, the competing climate mode, and the parallel mediator. The results show that this separable component is small at monthly resolution.

The low Qout–Ekman VIF and minimal shared commonality contribution rule out severe mediator collinearity as the principal cause. Instead, Niño3.4/DMI and their associated large-scale circulation fields appear to contain information shared simultaneously with ITF transport, atmospheric forcing, and Banda Sea OHC. Consequently, a simple serial pathway is an incomplete statistical representation of the coupled system.

## 3. Oceanic versus atmospheric pathways

The mechanistic diagnostics identify both oceanic and atmospheric pathways. Short-lag ITF–OHC coupling is compatible with oceanic redistribution of heat, while full Ekman pumping and wind stress provide a strong atmospheric pathway affecting upper-ocean structure. Directionality tests further indicate that atmospheric variability can precede ITF changes for several sections. These findings favor a network in which oceanic and atmospheric responses coexist and share remote climate forcing.

The absence of robust formal mediation should therefore not be interpreted as evidence that ITF transport or Ekman pumping is physically unimportant. It means only that their unique indirect contributions cannot be isolated robustly with the present monthly observational/reanalysis path model.

## 4. Robust, conditional, and exploratory evidence

Primary conclusions are restricted to findings classified as ROBUST/CORE after lag, preprocessing, FDR, seasonal, and event-level checks. CONDITIONAL/SUPPORTING findings are retained where effects are physically coherent but depend on adjustment, season, or model specification. Exploratory results—including non-robust mediation pathways—are used to constrain interpretation rather than to support confirmatory causal claims. This hierarchy reduces the risk of selecting isolated significant results from a large family of lagged and mechanistic tests.

## 5. Implications and limitations

The study provides a reproducible 1993–2025 framework linking validated native-grid ITF transport, ENSO/IOD variability, Banda Sea heat content, and atmospheric upwelling forcing. Important limitations remain. Reanalysis transport is not equivalent to direct mooring observation; monthly averaging may obscure faster adjustment processes; section geometry introduces transport uncertainty; and statistical directionality or mediation cannot establish physical causality. Future work should combine higher-frequency observations, process-model experiments, and targeted perturbation experiments to distinguish remote climate forcing from oceanic and atmospheric transmission mechanisms.

## Synthesis

Overall, the evidence supports strong and seasonally structured ENSO/IOD teleconnections to the Indonesian Throughflow and Banda Sea state. ITF transport and atmospheric forcing are physically coherent components of this response, but neither total outflow nor full Ekman pumping emerges as a statistically separable mediator of the climate–OHC relationship at monthly resolution. The most defensible interpretation is therefore a coupled climate–ocean–atmosphere response network rather than a single serial mediation pathway.
"""
 (ROOT/'manuscript/Results_Discussion_DRAFT.md').write_text(txt,encoding='utf-8')
 print('WROTE manuscript/Results_Discussion_DRAFT.md')
if __name__=='__main__':main()
