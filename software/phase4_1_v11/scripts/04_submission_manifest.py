from common import *
def main():
    rows=[]
    figs=[
      ("Figure_1_ITF_Validation.png","MAIN","Validation","Core"),
      ("Figure_2_ENSO_IOD_to_ITF.png","MAIN","Climate→ITF teleconnection","Core"),
      ("Figure_3_Seasonal_Event_Structure.png","MAIN","Seasonal/event modulation","Core"),
      ("Figure_4_ITF_Atmosphere_Banda_Coupling.png","MAIN","Mechanistic coupling","Core/supporting"),
      ("Figure_5_Integrated_Synthesis.png","MAIN","Integrated synthesis + mediation constraint","Core/context")
    ]
    tabs=[
      ("Table_1_ITF_validation_summary.csv","MAIN","Transport validation","Core"),
      ("Table_2_Core_ENSO_IOD_ITF_findings.csv","MAIN","Core climate→ITF results","Core"),
      ("Table_3_Seasonal_and_Banda_Coupling_Synthesis.csv","MAIN","Seasonal + Banda coupling synthesis","Core/supporting")
    ]
    for n,purpose,role,evidence in [(x[0],"figure",x[2],x[3]) for x in figs]:
        path=ROOT/"figures"/n
        rows.append({"artifact":n,"artifact_type":"figure","placement":"MAIN","scientific_role":role,
                     "evidence_level":evidence,"path":str(path),"exists":path.exists()})
    for x in tabs:
        path=ROOT/"tables"/x[0]
        rows.append({"artifact":x[0],"artifact_type":"table","placement":"MAIN","scientific_role":x[2],
                     "evidence_level":x[3],"path":str(path),"exists":path.exists()})
    for n in ["Figure_Captions.md","Table_Notes.md"]:
        path=ROOT/"captions"/n
        rows.append({"artifact":n,"artifact_type":"text","placement":"SUBMISSION_SUPPORT","scientific_role":"Captions/notes",
                     "evidence_level":"NA","path":str(path),"exists":path.exists()})
    out=pd.DataFrame(rows)
    out.to_csv(ROOT/"reports/submission_manifest.csv",index=False)
    if not out.exists.all():
        raise RuntimeError("Submission manifest has missing artifacts")
    print(out.to_string(index=False))
if __name__=="__main__":main()
