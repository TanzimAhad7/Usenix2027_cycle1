"""Build provenance and claim ledgers from the read-only reconstruction inputs."""
import csv, hashlib, json, re, shutil
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'IEEE_SP_Adversarial_Reconstruction_20261030'
PRIOR=ROOT/'IEEE_SP_Global_Audit_20261030'
LATEST=ROOT/'gemma_run_211739/gemma_completion_gpu2_20261029T211739Z_1117045_8864'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,x):p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def csvout(p, rows):
    with p.open('w',newline='')as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)

def main():
    shutil.copytree(PRIOR,OUT/'retained_global_audit',dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
    rows=[]
    candidates=[
        ('original_manuscript',ROOT/'global_audit_inputs/S&p rejected usenix/sec27cycle1-paper2797.pdf',
         'Full text read in preceding audit; scientific claims and decisive passages reopened in this reconstruction. Not a new full appendix reread.'),
        ('original_reviews',ROOT/'global_audit_inputs/S&p rejected usenix/USENIX Security 27 Cycle.txt','Both reviews completely reread.'),
        ('retrieved_v6',ROOT/'adversarial_reconstruction_inputs/IEEE_SP_Standalone_Research_Plan_v6_2026-10-07.md','Complete text read; header is revised 19 October despite filename.'),
        ('incident',ROOT/'adversarial_reconstruction_inputs/S&p rejected usenix/hugging-face-incident-report-aug-2026(2).pdf','All 91 extracted pages read, including appendices/footnotes. Selected pages visually checked. Raw 0:27000 and contiguous 27000:49000:71000:101000:132000:164000:197000:228000:end; whitespace normalized in later chunks.'),
        ('permissions_paper',ROOT/'reconstruction_work/literature/permissions.pdf','All 19 pages of scientific text, references, appendices and meta-review read fresh. Selected visual tables/figures.'),
        ('plugins_paper',ROOT/'reconstruction_work/literature/plugins.pdf','All 20 pages of scientific text, references, appendices and meta-review read fresh. Selected visual tables/figures.'),
        ('preceding_authority',OUT/'provenance/Authority_Before_This_Audit.md','Complete text freshly reread and challenged.'),
        ('current_source',LATEST/'source/retained/reference_discovery_parallel/base/vendor/AttriGuard.py','Decisive attenuation, comparison, exact fast path, parsing and history synchronization reopened; not a full new model/runtime reproduction.'),
        ('current_factory',LATEST/'source/retained/reference_discovery_parallel/base/vendor/my_agent_pipeline.py','Auxiliary factory/default and source settings inspected.'),
    ]
    for role,p,coverage in candidates:
        rows.append(dict(role=role,path=str(p.relative_to(ROOT)),bytes=p.stat().st_size,sha256=sha(p),coverage=coverage))
    write(OUT/'provenance/INSPECTED_INPUTS.json',rows)
    lit=[dict(title='Towards Automating Data Access Permissions in AI Agents',authors='Yuhao Wu; Ke Yang; Franziska Roesner; Tadayoshi Kohno; Ning Zhang; Umar Iqbal',
        venue='IEEE S&P 2026; official accepted list verified',url='https://umariqbal.com/papers/permissions-sp2026.pdf',
        pages=19,coverage=rows[4]['coverage'],pdf_sha256=rows[4]['sha256'],external_artifact_reproduction=False),
        dict(title='When AI Meets the Web: Prompt Injection Risks in Third-Party AI Chatbot Plugins',authors='Yigitcan Kaya; Anton Landerer; Stijn Pletinckx; Michelle Zimmermann; Christopher Kruegel; Giovanni Vigna',
        venue='IEEE S&P 2026; official accepted list verified',url='https://arxiv.org/pdf/2511.05797',
        pages=20,coverage=rows[5]['coverage'],pdf_sha256=rows[5]['sha256'],external_artifact_reproduction=False)]
    lit+=json.loads((PRIOR/'derived/LITERATURE_COVERAGE.json').read_text())
    write(OUT/'provenance/LITERATURE_READING_COVERAGE.json',dict(
        current_reconstruction_full_papers=lit[:2],
        retained_previous_audit_coverage=lit[2:],
        scope='The retained coverage records describe the preceding audit, not a new full reading in this reconstruction.'))
    write(OUT/'provenance/EVIDENCE_GAPS.json',[
        dict(item='governed-agentic-ai-plans.md',status='Original not located',evidence='Exact-title and broader Library searches; V6 also says missing',used='Only derivative eleven-idea disposition, not original.'),
        dict(item='Untouched 7 October v6',status='Not located as untouched version',evidence='Retrieved filename header revised19October',used='Actual retrieved version only.'),
        dict(item='Selected original paths',status='17 absent in combined export',evidence='retained_global_audit/derived/SELECTION_SCOPE.json',used='Present hash-matching primitives; no missing-response recreation.'),
        dict(item='Independent human semantic review of new panel',status='Pending prospective task',evidence='No such new human adjudication performed in this audit',used='Required before future collection.'),
        dict(item='Closest published auxiliary profile reproduction',status='Not performed on current witnesses',evidence='Current all-local role settings differ from factory default',used='P0 dependency or narrower claim.'),
        dict(item='Live university server state',status='Unavailable',evidence='Archived completed status only',used='No live running/stopped claim.'),
    ])
    source=LATEST/'source/retained/reference_discovery_parallel/base/vendor/AttriGuard.py'
    lines=source.read_text().splitlines(); anchors=[]
    for label,start,end in [('fuzzy_criterion',188,216),('attenuation',432,466),('exact_fast_path_and_payload',467,505),('source_parsing',505,630)]:
        anchors.append(dict(label=label,path=str(source.relative_to(ROOT)),source_sha256=sha(source),start_line=start,end_line=min(end,len(lines)),
            text='\n'.join(f'{i+1}: {lines[i]}'for i in range(start-1,min(end,len(lines))))))
    write(OUT/'derived/SOURCE_ANCHORS.json',anchors)
    # Each row distinguishes observations, inference and the missing stronger test.
    data=[
      ('C01','Controlled source sensitivity','observation','direct','retained_global_audit/derived/TOKEN_SCORE_RECHECK.json; HISTORICAL_PRIMITIVES.json; FRONTIER_*.json','U420 protection does not follow the source-risk narrative','Reconstructed scalar, information removal rather than changed permission','Faithful original-system transport and continuous effects bridge','Strong within design, token arithmetic independently rebuilt','The reconstructed score changes under a permission-preserving source intervention.','Evaluate the intended complete system; do not generalize to every causal defense.'),
      ('C02','Broad harmful guard claim','unsupported generalization','contradicted','retained_global_audit/derived/HISTORICAL_PRIMITIVES.json; CURRENT_E3_BOUNDS.json','Original U420 protection and Qwen worst-case protective bound','Guard protects most selected cases despite residual failures','Defined population and all-attempt matched comparison','Strong evidence against universal harm, no population claim','The guard protects recorded cases and has recorded exceptions.','New root-level workflow accounting with coverage/utility.'),
      ('C03','Seven latest guarded violations','observation','direct','derived/ZERO_PREFIX_WITNESSES.json; retained_global_audit/derived/CURRENT_SEVEN_PATHS.json','Matched guarded neutral neighbors nonviolating','Task/profile artifact, ordinary actor/ref error','Supported profile and held-out workflows','Strong finite-contract existence evidence','Seven recorded guarded target-bearing paths across six profile-root pairs commit forbidden simulated effects.','Faithful profile transport and independently authored tasks.'),
      ('C04','Consumption required for latest failures','hypothesis rejected as necessity','contradicted','derived/ZERO_PREFIX_WITNESSES.json','All seven sensitive prefixes are zero','First-dispatch semantic or reference failure','No new consumption experiment needed to reject necessity in these seven','Strong native-state check for these records','These seven failures do not require a prior sensitive commit.','Richer claim would need separate state intervention elsewhere.'),
      ('C05','Hostile text causes bad reference','causal hypothesis','plausible','derived/DELIVERED_INPUTS.json; SOURCE_ANCHORS.json','Lawful-reference fuzzy failures; many protected inputs','Local model error, salience, profile settings','P1 facts-fixed entire-pipeline carrier intervention','Input exposure certain; causal use unestablished','Delivered reference inputs retain hostile descriptions in exact witnesses.','Matched intervention, fact-preservation certificate and complete raw stages.'),
      ('C06','Exact bad-reference admission','program mechanism','direct','derived/ZERO_PREFIX_WITNESSES.json; SOURCE_ANCHORS.json','Protected cases may never generate exact bad reference','Intentional attribution criterion, not full policy guarantee','Upstream reference intervention and practical scope','Strong branch witness, elementary implication','An exact bad reference suffices for source admission of the held matching forbidden candidate.','Natural upstream causation and faithful configuration.'),
      ('C07','Lawful reference sufficient for safety','hypothesis rejected as sufficiency','contradicted','retained_global_audit/derived/CURRENT_PANEL_SUMMARY.json; CURRENT_SEVEN_PATHS.json','20 Gemma E2 harmful lawful-reference cells; two autonomous fuzzy witnesses','Criterion package, ordinary task error or anchoring','P2 matched criterion and task-only controls','Strong counterexamples under finite contracts','Lawful references do not ensure safe source admission in these records.','Neutral semantics and held-out comparator transport.'),
      ('C08','Paired Gemma E2 effect invariance','empirical regularity','direct','derived/PAIRED_E2.json','Qwen differs in five of56 pairs','Selected roots, deterministic/repeated settings','Fresh crossed reference/admission intervention','Strong descriptive 56/56 equality; causal universality absent','All56 selected Gemma origin/draw pairs have identical new-forbidden-effect counts across views.','New reference interventions and fresh roots.'),
      ('C09','Route substitution','empirical regularity','direct','derived/PAIRED_E2.json: DM_UPFRONT_K2_R01_MAIN_PARAMETER_RELEASE_NONE','One origin, four draws; correlated selection','Not independent random-token coupling','P1/P2 crossed path intervention','Strong recorded branch change, not an inferred hidden cause','Four pairs switch lawful/fuzzy to unlawful/exact while each commits two new forbidden effects.','Demonstrate an actual stage intervention has the same consequence elsewhere.'),
      ('C10','Evidence universally improves safety','hypothesis','contradicted','retained_global_audit/derived/CURRENT_E1_DETAIL.json; derived/PAIRED_E2.json','E1 ROOT and DESIGNATED move opposite ways; paired Gemma harm unchanged','Approval language, repetition, authority labels','Neutral fact/policy labels and discriminative component controls','Strong nonmonotonic diagnostic; strict E1 gate failed','The tested evidence addition does not uniformly improve source admission.','Separate content, structure and authority cue if claiming their mechanism.'),
      ('C11','E1 ambiguity explains all E3','hypothesis','contradicted','derived/ZERO_PREFIX_WITNESSES.json; GP/gemma/E1/E1_CHANNEL_PARAMETER_FORBID_ROOT_SOURCE_D1/item.json','Seven E3 roots exclude the target from genuine permitted alternatives','E1 ambiguity local, E3 semantics different','P0 independent semantic adjudication','Strong structural difference, human validation still prospective','E1 approval ambiguity cannot automatically invalidate the seven E3 contracts.','Independent meaning adjudication and source scope.'),
      ('C12','Review-skip unauthorized consequences','mechanistic interpretation','indirect','retained_global_audit/derived/HISTORICAL_PRIMITIVES.json; V6 review-skip discussion','15/2/1 labels final containing-run outcomes, not per-call permission','Final outcome may come from other actions','Call/event/contract join for each skipped privileged action','Source transition strong; call authorization unresolved','18/168 relevant privileged calls skip ordinary review; per-call authorization is not fully adjudicated.','Rebuild call-level consequence with actual runtime state.'),
      ('C13','Guard-specific overshoot','causal hypothesis','contradicted as unique explanation','retained_global_audit/derived/RECOVERY_AND_TRANSFER_DETAIL.json','Ordinary service interruption replicates selected Qwen overshoot','Generic recovery error and feedback state','Matched security/service inputs plus fresh independent tasks','Conditional local intervention evidence, not uniqueness','Admission and interruption can change recovery in selected traces.','Unique-security claim requires a difference beyond service interruption.'),
      ('C14','Reference occurrence reuse','conditional mechanism','direct','retained_global_audit/derived/S1_RECHECK.json','Native autonomous S1 never proposes intended duplicate','Known scoped-permission omission; candidate supplied','Fresh autonomous reachability only if mechanism remains central','Strong native conditional result, low novelty alone','16/16 held-excess conditions violate,13 with one reference occurrence.','Natural forbidden proposal plus source-qualified effect if claiming exploit.'),
      ('C15','Gemma missingness is random','assumption','contradicted','derived/MISSINGNESS.json; PHYSICAL_VS_REPORTING.json','42 failures in seven complete six-arm blocks','Schema/structure support','Complete-block named-profile reproduction if needed','Strong observed clustering, not a causal grammar attribution by itself','Missing outcomes are structured by root and cannot be ignored.','Qualified interface and all-attempt sensitivity.'),
      ('C16','Safe noncompletion means physical failure','interpretation','contradicted','derived/PHYSICAL_VS_REPORTING.json','14/17 Q and36/57 G qualified safe noncompletions physically complete','Reporting/contract/ordering mismatch','Independent separate physical/reporting endpoints','Strong native effect readout within finite predicate','Many safe noncompletions complete lawful physical effects but miss reporting.','Human meaning and complete prose-contract assessment.'),
      ('C17','Replay extreme groups are a new discovery','novelty/provenance claim','contradicted','V6 AppendixB.5; retained_global_audit/derived/REPLAY_RAW_SCOPE.json','Original v6 already explicitly reports unanimity','Recovered historical fact, not new replication','No experiment required to correct attribution','Strong document provenance','Replay groups are systematic extremes already recorded historically.','A new physical intervention, not threshold relabeling, for new science.'),
      ('C18','Incident proves causal-guard bypass','security claim','contradicted','provenance/INSPECTED_INPUTS.json: incident; incidentpp19,29,33','Causal scorer not deployed; execution compromise outside current threat model','Different trust/coordination problem','Separate mechanism reproduction needed','Strong limit from incident report; raw incident not independently reproduced','Incident motivates authority/provenance questions but does not demonstrate our guard failure.','In-scope implementation evidence, not analogy.'),
      ('C19','Every S&P paper needs new universal principle','venue standard claim','contradicted','provenance/LITERATURE_READING_COVERAGE.json; acceptedpapers meta-reviews','Accepted bounded empirical and independent-confirmation work','Important empirical novelty can suffice','Grounded significance and faithful controls for our own work','Primary full papers/meta-reviews inspected; no acceptance prediction','A bounded empirical security contribution can be valuable; our significance is unearned yet.','Important new exposure/boundary and convincing evidence.'),
      ('C20','Cross-guard unified mechanism','speculation','speculative','All audited families as a conceptual map','Different programs/tasks/measures; service and zero-prefix counterexamples','Several distinct mechanisms','Independent implementation plus shared discriminative prediction','Weak as unifying cause','The project supplies several related audit questions, not one identified root cause.','Measured bridge rather than pooled counts.'),
    ]
    fields=['id','claim','category','connection_strength','support','contradiction','alternative','missing_control','confidence_basis','maximum_wording','stronger_evidence']
    csvout(OUT/'derived/CLAIM_LEDGER.csv',[dict(zip(fields,x))for x in data])
    edges=[
        dict(origin='Zero-prefix native checkpoints',target='Prior sensitive consumption not necessary for seven witnesses',strength='directly demonstrated',limit='These seven records only'),
        dict(origin='Bad reference plus exact candidate equality',target='Source admission',strength='directly demonstrated',limit='Inspected source path; upstream cause not established'),
        dict(origin='Hostile procedure retained descriptively',target='Bad reference generation',strength='plausible',limit='Exposure not causal obedience'),
        dict(origin='Lawful reference plus explicit fuzzy true',target='Forbidden native effect',strength='directly demonstrated',limit='Two autonomous selected Gemma records'),
        dict(origin='Evidence-view intervention',target='General security improvement',strength='contradicted in tested general form',limit='Gemma pairs unchanged; other scopes open'),
        dict(origin='Selected guard interruption',target='Changed recovery',strength='conditional intervention evidence',limit='Ordinary service interruption can reproduce'),
        dict(origin='Original source score changes',target='Every later guard failure',strength='speculative',limit='No continuous cross-system causal chain'),
    ]
    csvout(OUT/'derived/EVIDENCE_MAP.csv',edges)
    print('Evidence package ledgers generated.')

if __name__=='__main__':main()
