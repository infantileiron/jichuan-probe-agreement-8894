from sqlalchemy import String,Text,JSON,ForeignKey,Double
from sqlalchemy.orm import Mapped,mapped_column
from .common import RecordMixin
from ..config.database import Base
class CalibrationStudy(RecordMixin,Base):
 __tablename__="studies"
 name:Mapped[str]=mapped_column(String(180),unique=True)
 dataset_id:Mapped[str]=mapped_column(ForeignKey("datasets.id"))
 instrument_id:Mapped[str]=mapped_column(ForeignKey("instruments.id"))
 variance_ratio:Mapped[float]=mapped_column(Double)
 tolerance:Mapped[float]=mapped_column(Double)
 # difference=原差值 y-x 分析（旧口径，兼容历史研究）；log_ratio=ln(y/x) 对数比值分析
 analysis_method:Mapped[str]=mapped_column(String(20),default="difference")
 # 仅对数比值分析使用：讨论容差，按相对偏差百分比解释，百分数存储（如10表示±10%）；差值分析为None
 relative_tolerance:Mapped[float]=mapped_column(Double,nullable=True)
