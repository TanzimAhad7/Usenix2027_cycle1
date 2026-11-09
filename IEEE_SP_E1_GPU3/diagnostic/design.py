from pathlib import Path
import copy,json
ROOT=Path(__file__).resolve().parents[1]
VIEWS=('MINIMAL','PLACEBO','DESIGNATED_FACTS_AND_PREFIX')
CRITERIA=('SOURCE','FORCED_SUPPORT','PERMISSION')

def manifest(draws=1):
    catalog=json.loads((ROOT/'diagnostic_inputs/CATALOG.json').read_text());p1=[];p2=[]
    for n,row in enumerate(catalog):
        for level in (2,3):
            p1.append(dict(id=f'X1_O{n:02d}_L{level}',panel='P1',stage='X1_REFERENCE_REGENERATION',origin=row['path'],level=level))
        for candidate in ('OBSERVED','LAWFUL_CONTROL'):
            for view in VIEWS:
                for criterion in CRITERIA:
                    for draw in range(draws):
                        p2.append(dict(id=f'X3_O{n:02d}_{candidate}_{view}_{criterion}_D{draw}',panel='P2',stage='X3_MATCHED_CHECKER',origin=row['path'],candidate_kind=candidate,view=view,criterion=criterion,draw=draw))
    # Constructed equal-view/opposite-policy controls, separate from authentic witnesses.
    for explicit in (False,True):
        for permitted in (False,True):
            for view in VIEWS:
                for criterion in CRITERIA:
                    for draw in range(draws):
                        p2.append(dict(id=f'X3_INFO_E{int(explicit)}_P{int(permitted)}_{view}_{criterion}_D{draw}',panel='P2',stage='X3_CONSTRUCTED_INFORMATION_CONTROL',explicit_rule=explicit,permitted=permitted,view=view,criterion=criterion,draw=draw))
    return dict(version=1,P1=p1,P2=p2,P3_blocks=[],draws=draws,origins=catalog,
        counts=dict(X1=len(p1),X3=len(p2)),independent_units='Eight outcome-selected checkpoints, not judge draws or population tasks',
        acquisition_scope='Exploratory conditional component diagnostics; no new autonomous attack-rate or confirmation claim',
        human_semantic_review='PENDING; no invented requirement to obtain a favorable human verdict before recording diagnostic evidence',
        information_scope='Facts and full native prefix added as a diagnostic information augmentation. No claim that source guard authenticates them or that a deployable policy compiler is supplied.',
        sampling_justification='One default draw identifies local route and diagnostic response; no stochastic reliability estimate. Additional draws remain nested and exploratory.',
        questions=['Missing input versus criterion under matched candidate/reference/state','Exact bypass versus forced review','Reference regeneration under recorded local role profiles','Known skip-state transition under scripted source/native fixtures'])
