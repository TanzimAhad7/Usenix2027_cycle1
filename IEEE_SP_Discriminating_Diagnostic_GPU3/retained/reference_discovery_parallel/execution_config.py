"""Execution settings are frozen, shared across all scientific conditions."""
WORKERS=2
GPU2_UUID='GPU-4d6b17a4-4e6c-95b7-972d-7807122ad7c6'
AUDIT_ALLOCATOR_MIB=256
AUDIT_SOFT_PROCESS_MIB=1024
AUDIT_MIN_FREE_MIB=2048

class DrainBeforeRestart(Exception):pass
