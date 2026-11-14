-- Reviewed upgrade for existing deployments (new databases are created from SQLAlchemy metadata).
-- Adds selectable agreement analysis to studies:
--   difference  = original Bland-Altman on raw differences d=y-x (legacy default)
--   log_ratio   = log-ratio Bland-Altman on z=ln(y/x), geometric mean ratio and ratio LoA
-- relative_tolerance is a percentage (e.g. 10 means +/-10% relative deviation) used only by log_ratio.
-- Deming regression always stays on the original readings; no stored run result is rewritten.
ALTER TABLE studies
  ADD COLUMN analysis_method VARCHAR(20) NOT NULL DEFAULT 'difference',
  ADD COLUMN relative_tolerance DOUBLE NULL;
-- Historical rows keep analysis_method='difference', so old runs and approved report snapshots
-- continue to read back exactly as saved. No backfill of run results is performed.
