from flask import render_template,request
from app import store
from app.pipeline import run
from app.config import TITLE,MODULES,STAGES,COLUMNS,SAMPLES,DEFAULTS
def view(stage):
    if not 1<=stage<=7: return "页面不存在",404
    run_id=request.args.get("run")
    result=store.fetch(run_id) if run_id else run()
    sample=(SAMPLES/"dirty.csv").read_text(encoding="utf-8-sig")
    data=result["stages"][stage-1]
    from datetime import datetime
    items=result["intervals"]
    start=min((datetime.fromisoformat(x["start"]).timestamp() for x in items),default=0)
    end=max((datetime.fromisoformat(x["end"]).timestamp() for x in items),default=1)
    tracks=[]
    for bed in sorted({x["bed"] for x in items}):
        bars=[]
        for x in items:
            if x["bed"]==bed:
                bars.append({**x,"left":(datetime.fromisoformat(x["start"]).timestamp()-start)/(end-start or 1)*100,"width":(datetime.fromisoformat(x["end"]).timestamp()-datetime.fromisoformat(x["start"]).timestamp())/(end-start or 1)*100})
        tracks.append({"bed":bed,"bars":bars})
    return render_template(f"m{stage}.html",title=TITLE,modules=MODULES,stage=stage,result=result,data=data,
                           sample=sample,defaults=DEFAULTS,columns=COLUMNS,history=store.history(),tracks=tracks)
