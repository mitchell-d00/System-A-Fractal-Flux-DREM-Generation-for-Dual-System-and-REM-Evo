# System A: Fractal Flux / DREM Generation for Dual System and REM-Evo

## 🎯 Project Overview

This repository contains the formal specification and implementation framework for **System A**, a constrained generative architecture designed to produce optimized candidate populations for downstream selection by **System B** (REM-Evo and constraint-based pruning systems).

System A does not evaluate correctness or truth. Instead, it transforms a seed structure into a bounded set of admissible candidate models through:

- **Recursive continuation** – expanding structural neighborhoods
- **Scale transformation** – adapting across different scales
- **Stabilization** – enforcing constraint satisfaction
- **Discriminability-driven branching (DREM)** – maximizing inter-candidate separability

The objective is to produce candidate sets that lie on the **Pareto frontier** of:
1. **Evaluability density** – the proportion of candidates decidable by System B
2. **Structural quality** – diversity, discriminability, and failure-mode richness

---

## 📋 Core Concepts

### System A Mapping

$$\text{System A}:(S,C)\mapsto K$$

Where:
- **S**: Initial seed structure
- **C**: Constraint vocabulary (domain specification)
- **K**: Optimal candidate set (on Pareto frontier)

### Key Design Principles

| Principle | Description |
|-----------|-------------|
| **Admissibility** | All candidates must satisfy intervention-decomposability, test exposure, and constraint compliance |
| **Bounded Expansion** | Candidate population growth is algorithmically controlled via branching constraints |
| **Discriminability** | Candidates are explicitly designed to be distinguishable under evaluation conditions |
| **Evaluability** | Candidates are optimized for decisive resolution by downstream systems |
| **Structural Legibility** | All candidates expose explicit assumptions, predictions, and failure conditions |

---

## 🏗️ Architecture

### Layered Design

#### Specification Layer
- Explicit assumptions, testable predictions, and failure conditions
- Structural decomposability
- Cross-candidate comparability

#### Operator Layer
- **Φ_E** (Continuation): Expand neighborhoods via admissible rewrites
- **𝔉_E** (Scale Transformation): Adapt across scale domains
- **𝒮_H** (Stabilization): Repair constraint violations
- **D_E** (DREM Branching): Generate discriminable variants

#### Implementation Layer
- Domain-specific definitions of cost functions, instability functionals
- Representation maps (ψ) for comparing candidates
- Evaluation procedures (𝓔) for assessing decisiveness

---

## 📐 Candidate Space

All candidates **k** are 5-tuples:

$$k = (A, B, R, P, F)$$

| Component | Meaning |
|-----------|---------|
| **A** | Explicit assumptions (subset of C) |
| **B** | Bounds on parameters/scope |
| **R** | Structural relations |
| **P** | Testable predictions (non-empty) |
| **F** | Failure conditions (non-empty) |

**Invariant**: P ≠ ∅ and F ≠ ∅ ensure all candidates are both testable and falsifiable.

---

## ⚙️ Operational Dynamics

### Single Iteration

$$K_{t+1} = \Pi_M \circ D_E \circ \mathcal{S}_H \circ \mathfrak{F}_E \circ \Phi_E (K_t)$$

1. **Continuation** (Φ_E): Expand each candidate via single-step transformations
2. **Scale Transformation** (𝔉_E): Generate scaled variants
3. **Stabilization** (𝒮_H): Repair constraint violations via minimal-cost repairs
4. **DREM Branching** (D_E): Select high-discriminability transformation axes
5. **Admissibility Filter** (Π_M): Retain only admissible candidates

### Constraints

- **Bounded Expansion**: $|K_{t+1}| \le b_{max} |K_t|$
- **Branch Entropy**: $H_{branch}(K_t) \ge h_{min}$ (ensures diversity in branching axes)

---

## 📊 Quality Metrics

### Evaluability Density

$$\rho_E(K) = \frac{1}{|K|} \sum_{k \in K} M(k) \cdot \mathcal{E}(k)$$

Fraction of admissible candidates decisively resolvable by System B.

### Discriminability

$$\mathrm{Disc}(K) = \frac{2}{|K|(|K|-1)} \sum_{i<j} \mathcal{D}(k_i, k_j)$$

Average pairwise separation under representation map ψ.

### Diversity

$$\mathrm{Div}(K) = \text{Coverage across structural families in } (A, R, F)$$

Breadth of assumption/relation/failure-mode families.

### Combined Quality

$$Q(K) = \lambda_1 \mathrm{Div}(K) + \lambda_2 \mathrm{Disc}(K) + \lambda_3 \overline{\mathrm{Exp}} + \lambda_4 \overline{\mathrm{Scale}} + \lambda_5 \overline{\mathrm{Fail}}$$

Weighted aggregation of structural properties.

---

## 🎲 DREM (Discriminability-Reachability-based Expansion Model)

DREM guides branching via axis selection:

### Axis Selection Process

For each candidate **k**:

1. **Enumerate axes**: $X(k) = \{x | x \text{ is a parameterized transformation family}\}$
2. **Compute discriminability gain**:
   $$\mathbb{E}[\Delta \mathcal{D}_B | x, C] = \mathbb{E}_{\theta, \theta'} [\mathcal{D}_B(k(x,\theta), k(x,\theta'))]$$
3. **Score axes (cost-aware)**:
   $$\mathrm{score}(x) = \frac{\mathbb{E}[\Delta \mathcal{D}_B | x, C]}{\mathrm{cost}(x) + \epsilon}$$
4. **Select top-m axes** and generate variants

### System B Alignment

Discriminability is computed w.r.t. **predicted evaluative outcomes**, ensuring branching directly optimizes for downstream resolvability.

---

## ✅ Admissibility Conditions

A candidate **k** is admissible ($M(k) = 1$) iff:

1. **Representation Preservation**: ∃ set of identity-preserving transformations
2. **Intervention Decomposability**: Bounded and legible causal structure
3. **Test Exposure**: Discriminative predictions over evaluation conditions
4. **Constraint Compliance**: $A, B \subseteq C$

Projection operators:
- $\Pi_M(K)$ – strictly admissible candidates
- $\Pi_{M,\epsilon}(K)$ – ε-relaxed admissibility

---

## ⚠️ Failure Modes

| Failure Mode | Signature | Cause |
|--------------|-----------|-------|
| **Noise Expansion** | $\|K\| \uparrow, \mathrm{Disc}(K) \downarrow$ | Branching on low-signal axes |
| **Convergence Collapse** | $\|K\| \to 1$ | Over-aggressive stabilization |
| **Semantic Drift** | $P \to \emptyset, F \to \emptyset$ | Erosion of testability |
| **Hidden Constraints** | $A \not\subseteq C$ | Implicit assumptions not exposed |

**Mitigation strategies** are implementation-specific and should be defined per domain.

---

## 📁 Repository Structure

```
.
├── README.md                          # This file
├── SYSTEM_A_SPECIFICATION.md          # Complete formal specification
├── docs/
│   ├── architecture.md                # Detailed architecture walkthrough
│   ├── operators.md                   # Operator semantics and properties
│   ├── admissibility.md               # Admissibility framework
│   └── failure_modes.md               # Failure mode analysis
├── src/
│   ├── core/
│   │   ├── candidate.py               # Candidate data structures
│   │   ├── operators.py               # Operator implementations
│   │   └── dynamics.py                # Iteration and reachable set
│   ├── drem/
│   │   ├── axis_selection.py          # DREM axis enumeration
│   │   ├── discriminability.py        # Discriminability metrics
│   │   └── branching.py               # Branching policy
│   └── examples/
│       └── minimal.py                 # Minimal working example
└── tests/
    ├── test_operators.py
    ├── test_admissibility.py
    └── test_drem.py
```

---

## 🚀 Getting Started

### Installation

```bash
git clone https://github.com/mitchell-d00/System-A-Fractal-Flux-DREM-Generation-for-Dual-System-and-REM-Evo
cd System-A-Fractal-Flux-DREM-Generation-for-Dual-System-and-REM-Evo
pip install -e .
```

### Minimal Example

```python
from system_a import System, Candidate, Constraints

# Define constraints
C = Constraints(vocabulary=["param_x", "param_y", "relation_R"])

# Initialize seed
seed = Candidate(
    assumptions={"param_x > 0"},
    bounds={"x": (0, 100)},
    relations={"R": "linear"},
    predictions={"output: y ≈ 2x"},
    failures={"output: y ≈ 2x fails when x > 50"}
)

# Run System A
system = System(
    seed=seed,
    constraints=C,
    max_iterations=10,
    b_max=2.0  # branching factor
)

K_star = system.run()
print(f"Generated {len(K_star)} candidates")
```

---

## 📖 Documentation

- **[SYSTEM_A_SPECIFICATION.md](./SYSTEM_A_SPECIFICATION.md)** – Complete formal specification with all definitions and theorems
- **[Architecture Guide](./docs/architecture.md)** – Detailed walkthrough of the layered design
- **[Operator Reference](./docs/operators.md)** – Semantics and correctness properties
- **[Admissibility Framework](./docs/admissibility.md)** – Conditions and verification
- **[Failure Modes & Mitigation](./docs/failure_modes.md)** – Common pitfalls and solutions

---

## 🔄 Workflow with System B (REM-Evo)

System A is designed as the **candidate generation** phase in a two-stage process:

```
Seed (S, C)
    ↓
[SYSTEM A: Candidate Generation]
    ↓ K = {k₁, k₂, ..., kₙ}
    ↓
[SYSTEM B / REM-Evo: Selection & Evaluation]
    ↓
Best candidate (or ensemble)
```

**System A ensures**:
- All candidates are testable and distinguishable
- Evaluation budget is efficiently allocated
- High-probability candidates for decisiveness are prioritized

**System B provides**:
- Ground-truth evaluation against data/experiments
- Constraint pruning and refinement
- Final model selection

---

## 🤝 Contributing

Contributions are welcome. Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit changes with clear messages
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

---

## 📝 Citation

If you use System A in your research, please cite:

```bibtex
@article{system-a-2026,
  title={System A: Fractal Flux / DREM Generation for Dual System and REM-Evo},
  author={Your Name},
  year={2026},
  note={GitHub: mitchell-d00/System-A-Fractal-Flux-DREM-Generation-for-Dual-System-and-REM-Evo}
}
```

---

## 📄 License

This project is licensed under the MIT License – see LICENSE file for details.

---

## ❓ Questions & Support

- **Issues**: Report bugs or request features via [GitHub Issues](https://github.com/mitchell-d00/System-A-Fractal-Flux-DREM-Generation-for-Dual-System-and-REM-Evo/issues)
- **Discussions**: Join conversations in [GitHub Discussions](https://github.com/mitchell-d00/System-A-Fractal-Flux-DREM-Generation-for-Dual-System-and-REM-Evo/discussions)
- **Email**: Contact repository maintainer

---

**Last Updated**: May 24, 2026  
**Status**: Active Development
