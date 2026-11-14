from pydantic import BaseModel,Field,model_validator
class StudyCreate(BaseModel):
 name:str=Field(min_length=2,max_length=180)
 dataset_id:str
 instrument_id:str
 variance_ratio:float=Field(default=2.25,gt=0,le=1000000,allow_inf_nan=False)
 tolerance:float=Field(default=2,gt=0,le=1000000,allow_inf_nan=False)
 analysis_method:str=Field(default="difference",pattern="^(difference|log_ratio)$")
 relative_tolerance:float|None=Field(default=None,gt=0,le=100,allow_inf_nan=False)
 @model_validator(mode="after")
 def check_method_tolerance(self):
  if self.analysis_method=="log_ratio" and self.relative_tolerance is None:raise ValueError("对数比值分析必须填写相对容差（相对偏差百分比）")
  return self
