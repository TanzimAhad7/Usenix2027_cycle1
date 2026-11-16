"""Execution settings are frozen, shared across all scientific conditions."""
WORKERS=2
GPU2_UUID='GPU-0b687901-110f-39c5-a5a9-dfe4b73cc932'
AUDIT_ALLOCATOR_MIB=256
AUDIT_SOFT_PROCESS_MIB=1024
AUDIT_MIN_FREE_MIB=2048

class DrainBeforeRestart(Exception):pass
