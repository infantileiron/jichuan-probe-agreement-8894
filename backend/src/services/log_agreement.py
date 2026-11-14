import math

# 对数比值（log-ratio）Bland–Altman 分析：
# 配对样本按 z=ln(y/x) 变换并聚合，偏倚与样本标准差在对数尺度计算，
# 再指数还原为几何均比 exp(mean z) 与一致性比值界限 exp(mean z ± 1.96 sd)。
# 容差按相对偏差百分比解释：|y/x - 1| > 容差分数 即标记越界。
# 任一读数含零或负值时对数无定义，整次运行明确失败（由调用方落为 failed）。

def analyze(x,y,relative_tolerance):
 if len(x)!=len(y) or len(x)<4:raise ValueError("对数比值分析至少需要4组配对")
 if not all(math.isfinite(v) for v in x+y):raise ValueError("读数必须有限")
 if not math.isfinite(relative_tolerance) or relative_tolerance<=0:raise ValueError("相对容差须为正的有限百分数")
 for index,(a,b) in enumerate(zip(x,y),1):
  if a<=0 or b<=0:raise ValueError(f"对数比值分析要求全部读数严格为正：第{index}对含零或负值(x={a}, y={b})，本次运行失败")
 n=len(x)
 log_ratios=[math.log(b/a) for a,b in zip(x,y)]
 log_means=[(math.log(a)+math.log(b))/2 for a,b in zip(x,y)]
 bias=math.fsum(log_ratios)/n
 sd=math.sqrt(math.fsum((z-bias)**2 for z in log_ratios)/(n-1))
 log_low=bias-1.96*sd;log_high=bias+1.96*sd
 ratio_low=math.exp(log_low);ratio_high=math.exp(log_high)
 mg=math.fsum(log_means)/n;ss=math.fsum((g-mg)**2 for g in log_means)
 if ss==0:proportional={"estimable":False,"slope":None,"intercept":None,"r_squared":None,"reason":"两探头对数几何均值为常量，比例趋势回归不可估计"}
 else:
  slope=math.fsum((g-mg)*(z-bias) for g,z in zip(log_means,log_ratios))/ss;intercept=bias-slope*mg
  residual_sse=math.fsum((z-intercept-slope*g)**2 for g,z in zip(log_means,log_ratios));total_ss=math.fsum((z-bias)**2 for z in log_ratios)
  proportional={"estimable":True,"slope":slope,"intercept":intercept,"r_squared":None if total_ss==0 else max(0.,min(1.,1-residual_sse/total_ss)),"reason":""}
 outside_loa=sum(z<log_low or z>log_high for z in log_ratios)
 outside_tolerance=sum(abs(math.exp(z)-1)>relative_tolerance for z in log_ratios)
 return {"analysis_method":"log_ratio","n":n,"transformation":"ln(y/x)","log_bias":bias,"log_sample_sd":sd,"log_loa_low":log_low,"log_loa_high":log_high,"geometric_mean_ratio":math.exp(bias),"ratio_loa_low":ratio_low,"ratio_loa_high":ratio_high,"outside_loa":outside_loa,"relative_tolerance_pct":relative_tolerance*100,"outside_tolerance":outside_tolerance,"proportional":proportional,"sd_ddof":1,"limits_note":"ln(y/x)均值 ± 1.96 × 样本SD，指数还原为比值界限；界限不是置信区间，不直接证明设备可互换。容差为相对偏差百分比，非原读数绝对差。"}
