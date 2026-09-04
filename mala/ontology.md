# MALA Inspection Ontology

## Classes (エンティティ)

### Agent
- Inspector (インスペクター)
- Experimenter (実験者)
- BoundaryAnalyst (境界分析者)
- EvidenceCollector (証拠収集者)
- PatternGeneralizer (パターン一般化者)

### Process
- Inspection (インスペクション)
- Observation (観察)
- Hypothesis (仮説)
- Experiment (実験)
- Comparison (比較)
- BoundaryLocation (境界特定)
- Explanation (説明)
- Generalization (一般化)
- Action (行動)
- Verification (検証)
- Recording (記録)

### Artifact
- Evidence (証拠)
- Pattern (パターン)
- Mismatch (不整合)
- Boundary (境界)
- ObservationRecord (観察記録)
- Reproduction (再現)
- Tool (ツール)
- Knowledge (知識)

## Properties (スロット)

### Agent → Process
- performs (実行する)
- validates (検証する)
- generalizes (一般化する)
- observes (観察する)

### Process → Artifact
- produces (生成する)
- requires (必要とする)
- basedOn (基づく)

### Artifact → Artifact (Relation)
- contradicts (矛盾する)
- supports (支持する)
- derivesFrom (派生する)
- matches (一致する)
- mismatches (不一致)

## Axioms (公理)

```
∀i: Inspection → ∃o: Observation ∧ ∃e: Evidence
∀e: Evidence → ∃r: Reproduction
∀m: Mismatch → ∃b: Boundary
∀p: Pattern → ∃g: Generalization ∧ ∃v: Verification
```

## Inspection Flow (状態遷移)

```
[Inspection] 
   1. triggered_by → Mismatch | UnknownBehavior | Contradiction
   2. observe → Observation
   3. hypothesize → Hypothesis[]
   4. experiment → Experiment (minimal)
   5. compare → Result (expected vs observed)
   6. locate_boundary → Boundary
   7. explain → Explanation (causal chain)
   8. generalize → Pattern (candidate)
   9. act → Action (fix | tool | test | rule)
  10. verify → Verification (PASS | FAIL | UNCERTAIN)
  11. record → Knowledge (with provenance)
```

## Boundary Types (境界分類)

| Type | Example |
|------|---------|
| ComponentBoundary | client / server |
| RepresentationBoundary | serialized / deserialized |
| TrustBoundary | trusted / untrusted |
| ProtocolBoundary | HTTP / application |
| ParserBoundary | parser / parser |
| AuthBoundary | authenticated / anonymous |

## Evidence Quality (証拠の質)

| Level | Criteria |
|-------|----------|
| Raw | 観察された事実 |
| Reproduced | 再現可能 |
| Causal | 原因が特定されている |
| Impact | 影響が評価されている |
| Verified | 修正後に検証済み |

## JSON-LD Template

```json
{
  "@context": "mala:ontology",
  "@type": "Inspection",
  "id": "INS-001",
  "trigger": {
    "type": "Mismatch",
    "boundary": "ProtocolBoundary",
    "observed": "...",
    "expected": "..."
  },
  "inspector": "Agent/Inspector-01",
  "steps": [
    {"@type": "Observation", "evidence": "..."},
    {"@type": "Experiment", "minimal": true, "result": "..."},
    {"@type": "BoundaryLocation", "boundary": "..."},
    {"@type": "Explanation", "cause": "...", "confidence": 0.9},
    {"@type": "Action", "type": "fix|tool|test|rule"},
    {"@type": "Verification", "status": "PASS"}
  ],
  "output": {
    "@type": "Pattern",
    "generalization": "...",
    "horizontal_expansion_targets": ["..."]
  }
}
```
