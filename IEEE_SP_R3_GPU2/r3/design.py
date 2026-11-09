import random
from .common import ROOT,read,digest
SETTINGS={'A':dict(error_aware=False,contract_gate=False),'B':dict(error_aware=True,contract_gate=False),'C':dict(error_aware=False,contract_gate=True),'D':dict(error_aware=True,contract_gate=True)}
LIMITS=dict(max_iters=15,max_model_queries=128,max_output_tokens=8192,max_model_len=32768,request_timeout_seconds=180,case_timeout_seconds=2400)
def manifest():
    jobs=[]
    for block in range(2):
        batch=[]
        for task in ('BANK','EMAIL'):
            for carrier in ('NEUTRAL','PARAMETER'):
                for setting in SETTINGS:
                    spec=read(ROOT/'fixtures'/f'{task}_{carrier}.json')
                    batch.append(dict(id=f'R3_{task}_{carrier}_A{block}_{setting}',kind='FULL',task=task,carrier=carrier,context=block,setting=setting,spec=spec,limits=LIMITS))
        random.Random(20261105+block).shuffle(batch);jobs.extend(batch)
    branches=[dict(id='R3_BRANCH_'+j['id']+'_'+s,kind='BRANCH',parent=j['id'],setting=s,task=j['task'],carrier=j['carrier'],context=j['context'],limits=LIMITS) for j in jobs if j['setting']=='A' for s in SETTINGS]
    return dict(schema='R3_DESIGN_V1',full_workflows=32,conditional_slots=32,independent_parent_maximum=8,model_configuration='OFFICIAL_LOCAL_QWEN_ALL_ROLES_SINGLE_ENDPOINT',settings=SETTINGS,limits=LIMITS,jobs=jobs,branches=branches,scope='Development discrimination, not a population-rate or unseen-task study; public-contract gate is a diagnostic oracle',manifest_content_sha256=digest(dict(jobs=jobs,branches=branches)))
