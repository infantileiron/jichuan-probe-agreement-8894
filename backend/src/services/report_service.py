import csv,io
from uuid import uuid4
from sqlalchemy import select
from fastapi import HTTPException
from ..models.review import BiasReview
from ..models.run import CalibrationRun
from ..models.report import Report

def create(db,body):
 review=db.get(BiasReview,body.review_id)
 if review is None or review.state!="approved":raise HTTPException(409,"报告必须关联已批准的偏倚复核")
 existing=db.scalar(select(Report).where(Report.review_id==body.review_id))
 if existing:return existing
 run=db.get(CalibrationRun,review.run_id);row=Report(id=str(uuid4()),review_id=review.id,title=body.title,snapshot={"result":run.result,"action":review.action,"reviewer":review.reviewer});db.add(row);db.commit();return row

def export(row):
 result=row.snapshot["result"];out=io.StringIO();writer=csv.writer(out);unit=result["unit"]
 # 历史快照可能没有 analysis_method 键，按原差值口径回读
 method=result.get("analysis_method") or "difference"
 if method=="log_ratio":
  pct=result.get("relative_tolerance_pct")
  writer.writerow([f"# 分析方式：对数比值Bland–Altman（逐对 ln(Y/X) 变换，几何均比与比值界限由指数还原）；Deming仍使用原{unit}读数"])
  writer.writerow([f"# 单位：{unit}；容差含义：相对偏差 ±{pct}%（|Y/X−1| 超过 {pct}% 即 outside_tolerance=True），不是{unit}绝对差"])
  writer.writerow(["pair_id","range_label","x","y","unit","ratio_y_over_x","log_ratio_ln_y_over_x","deming_fitted_y","residual_y","outside_ratio_loa","outside_relative_tolerance"])
  for p in result["points"]:writer.writerow([p["pair_id"],p["range_label"],p["x"],p["y"],unit,p["ratio_y_over_x"],p["log_ratio"],p["fitted_y"],p["residual_y"],p["outside_loa"],p["outside_tolerance"]])
 else:
  # 原差值口径（含无 analysis_method 键的历史报告）：列结构保持不变
  writer.writerow(["pair_id","range_label","x","y","unit","mean","difference_y_minus_x","deming_fitted_y","residual_y","outside_loa","outside_tolerance"])
  for p in result["points"]:writer.writerow([p["pair_id"],p["range_label"],p["x"],p["y"],unit,p["mean"],p["difference"],p["fitted_y"],p["residual_y"],p["outside_loa"],p["outside_tolerance"]])
 return "﻿"+out.getvalue()
