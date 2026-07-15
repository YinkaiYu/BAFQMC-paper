# Manuscript Story And Evidence Principles

Use this file for every part of the manuscript, including the abstract, Introduction, formalism, theorems, examples, benchmarks, conclusion, captions, Supplemental Material, and revision reports. Task-specific guides apply these principles but do not replace them.

## 1. Start From The Scientific Job

Before editing a section, paragraph, sentence, equation, or figure, state its job in the paper.

A useful unit should do at least one of the following:

- establish why the problem matters;
- create a question or obstacle that the paper resolves;
- supply the physical picture needed for a later result;
- state a result or assumption;
- explain why a result is true;
- turn a formal result into a physical or computational consequence;
- demonstrate that the method works;
- delimit a claim where the boundary affects interpretation or reproducibility.

Remove or rewrite material whose main purpose is to show that the authors know the literature, answer a collaborator's request, display rigor, or narrate the revision process.

## 2. Build A Causal Story

A scientific paper should read as a chain of necessity:

1. a consequential problem exists;
2. existing knowledge or methods leave a specific obstruction;
3. the paper introduces the idea that removes the obstruction;
4. the formal result makes that idea precise;
5. examples and data show that it works;
6. the conclusion states what can now be done or understood.

Each paragraph should have one dominant action. Arrange sentences so that each creates the need for the next. Use contrast, a question, or a reversal only when it changes the reader's understanding, not as decoration.

Do not let the conventional order of a literature review, derivation, code implementation, or chronological work log determine the order of the paper.

## 3. Control Reader Burden

Assume an intelligent theoretical physicist who is not already inside this project's notation or subfield.

- Introduce the physical object before its formal representation.
- Explain a new distinction before naming it with specialist terminology.
- Define symbols and assumptions before compact formulas rely on them.
- After a long gap, reintroduce the object needed locally instead of forcing a backward search.
- Prefer one additional explanatory step over an unexplained technical label.
- Remove definitions, variables, and caveats that are never used locally.
- Do not compress transitions until the argument becomes abrupt.
- Do not expand by listing terminology. Expand the causal or physical explanation.

Reader accessibility does not require elementary prose everywhere. It requires a controlled increase in technical depth.

## 4. Separate Layers Of Precision

Place information at the layer where it changes the reader's decision or understanding.

- **Title and abstract:** problem, result, reach, and strongest validation.
- **Introduction:** physical stakes, conceptual gap, central idea, main claims, and consequences.
- **Main formalism:** assumptions and formulas needed to understand and use the result.
- **Theorem statements:** assumptions and conclusions only.
- **Proof discussion:** mechanism and intuition at the shortest useful level.
- **Supplemental Material:** full derivations, branch conventions, convergence domains, stabilization, update formulas, parameters, and reproducibility details.
- **Research report:** alternative sources, rejected wording, citation counts, reviewer strategy, and caveats that would interrupt the paper.

Do not move every qualification upward in the name of rigor. A correct caveat is misplaced when it obscures the main result before the reader understands it. Conversely, never hide a condition that changes the truth of a claim.

## 5. Use Confidence Correctly

Confidence comes from selecting the strongest supportable claim and stating it directly.

- Prefer `we prove`, `we establish`, `we formulate`, and `the criterion guarantees` when the manuscript supplies the proof.
- Avoid `may`, `could`, `appears`, and procedural verbs when the result is established.
- Avoid inflated universality, priority, or impact claims that exceed the theorem or benchmark.
- Do not add habitual defensive qualifiers that are already implicit in standard field usage.
- Do not use disclaimers to pre-answer every imaginable referee objection.
- State a real limitation once, at the point where it affects interpretation, applicability, or reproducibility.

The target is bold and accurate, not timid and not promotional without evidence.

## 6. Make Evidence Serve Claims

Treat citations, equations, figures, and benchmarks as different forms of evidence.

- A citation supports known background, prior art, a physical target, or an external result.
- An equation defines or proves the manuscript's own formal claim.
- A schematic gives the reader a conceptual map.
- A benchmark validates an implementation or consequence at a stated evidence level.

Do not ask one form of evidence to prove something it does not establish. A phase paper does not prove a computational no-go. Agreement on a small benchmark does not establish a thermodynamic phase diagram. A review maps a field but does not replace an original theorem.

For each claim, identify the evidence obligation and attach evidence at the closest natural point. Broad citation clusters are acceptable; broad unsupported claims are not.

## 7. Research Widely, Write Selectively

The research process should be broader and more rigorous than the final prose.

1. Build the field map from original papers, reviews, reference chains, supplements, and recent work.
2. Record competing terminology, caveats, historical branches, citation counts, and active groups in the research report.
3. Decide what the reader needs for the paper's story.
4. Write the shortest coherent version that preserves the physical picture.
5. Audit the draft sentence by sentence for missing or mismatched evidence.

Do not transfer the structure of the research notes into the manuscript. The report stores breadth; the paper delivers a controlled argument.

## 8. Preserve Narrative During Citation Expansion

Adding references must not force extra review prose.

- Reuse sentences that already carry a legitimate broad claim.
- Place several papers in one cluster when they support the same statement.
- Split clusters only when the prose contains distinct evidence obligations.
- Put citations next to the item they support in a multi-example sentence.
- Keep strategically useful but weakly connected papers in the report-level candidate list.

Broad and socially aware citation coverage is compatible with rigorous writing when every cited paper has a defensible local role.

## 9. Design Figures For Reader Shortcuts

Many readers inspect the title, abstract, figures, and captions before reading the derivation.

- A conceptual figure should reveal the paper's organizing idea without private revision context.
- A data figure should make the comparison, parameters, observables, and evidence level clear.
- A caption should teach the figure, not defend the paper against hypothetical objections.
- Use neutral descriptive titles rather than slogans tailored to an author's feedback.
- Keep schematics simple enough to survive a quick scan.

The figure and caption may simplify presentation, but they must not contradict the formal result.

## 10. Edit Iteratively Without Losing Intent

For mature prose that has undergone several author iterations:

- identify the established narrative job before changing wording;
- avoid opportunistic rewrites triggered only by finding a new paper;
- prefer the smallest change that fixes the actual issue;
- compare substantive changes against the author-approved baseline, not the previous agent draft;
- after changing a sentence, update its citation analysis and report entry;
- after research changes the physics picture, revisit the prose rather than preserving an outdated sentence mechanically.

New evidence can justify a new sentence or a new structure, but the burden is to improve the reader's story, not merely to expose the research finding.

## 11. Section-Level Tests

### Abstract

Can a broad reader identify the problem, result, validation, and impact without specialist setup?

### Introduction

Does every paragraph increase the need for the paper and lead naturally to its result?

### Formalism

Does the reader know the physical operation before meeting the compact matrix formula?

### Theorem Or Criterion

Are assumptions and conclusion unmistakable, with intuition outside the formal statement?

### Example

Is it clear why this model satisfies the criterion and what new territory it represents?

### Benchmark

Is the evidence level explicit, and does the text explain what agreement validates?

### Conclusion

Does it synthesize the new capability and physical opportunity rather than repeat the abstract or list future work?

### Supplemental Material

Can a specialist reconstruct the derivation and implementation without relying on undocumented code knowledge?

## 12. Sentence Audit

Before finalizing important prose, ask:

1. What exact job does this sentence perform?
2. What must the reader already know?
3. What new need, result, mechanism, or consequence does it create?
4. Is its strongest claim supported at the right evidence level?
5. Is any qualification essential here, or does it belong later?
6. Would the sentence make sense to a reader who never saw the revision discussion?
7. Can it be shorter without losing the physical picture or logical bridge?

If the answers are unclear, revise the sentence before polishing its style.
