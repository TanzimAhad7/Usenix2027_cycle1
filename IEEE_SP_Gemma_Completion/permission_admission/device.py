"""Current completion placement; archived runtime files remain unchanged."""
GPU_INDEX = 2
GPU_UUID = 'GPU-0b687901-110f-39c5-a5a9-dfe4b73cc932'
LOCK_NAME = 'gpu2_sequence.lock'


def qualify_available(serving):
    gpu = next((row for row in serving.gpu_table()
                if row[0].strip() == str(GPU_INDEX)), None)
    if not gpu or gpu[1].strip() != GPU_UUID:
        raise RuntimeError('Physical GPU 2 does not match pinned UUID; no other GPU will be used')
    occupied = [row for row in serving.gpu_applications()
                if len(row) > 1 and row[1].strip() == GPU_UUID]
    if occupied:
        raise RuntimeError('GPU 2 has existing compute processes; none were stopped: ' + str(occupied))
    # The byte-preserved helper filters its telemetry using this module value.
    serving.GPU = GPU_INDEX
    return gpu
