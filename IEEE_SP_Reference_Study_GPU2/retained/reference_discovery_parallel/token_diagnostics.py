"""Diagnostics overlap generation without caching/reusing model outputs."""
import copy
from concurrent.futures import ThreadPoolExecutor

class Diagnostics:
    def __init__(self,work):self.work=work;self.pool=None;self.jobs=[];self.closed=False
    def submit(self,index,payload):
        if self.closed:raise RuntimeError('Diagnostic queue closed')
        if self.pool is None:self.pool=ThreadPoolExecutor(max_workers=1,thread_name_prefix='diagnostic_tokenize')
        self.jobs.append(self.pool.submit(self.work,index,copy.deepcopy(payload)))
    def close(self):
        self.closed=True
        if self.pool:self.pool.shutdown(wait=True)
        for job in self.jobs:job.result()
