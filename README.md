# RamSat: A Ramsey Theory Calculator  
### Computing Ramsey Numbers using the Pigeonhole Principle, Erdős Probabilistic Method, and SAT-Based Edge Coloring Verification

---

## Overview

**RamSat** is a computational framework designed to explore **Ramsey Theory** — the branch of combinatorics that reveals how **order inevitably emerges within sufficiently large structures**.

This project computes and verifies **Ramsey numbers** using a hybrid of mathematical and computational approaches:

- **Pigeonhole Principle Bounds**
- **Erdős’ Probabilistic Method**
- **SAT-Based Edge Coloring Verification**
- **Combinatorial Bound Analysis**

RamSat aims to bridge **theoretical mathematics** and **computational verification**, providing an experimental platform for studying the transition from randomness to structure.

---

## Features

- ✅ Compute **upper and lower bounds** for Ramsey numbers  
- ✅ Simulate **random edge colorings** using probabilistic analysis  
- ✅ Verify **small Ramsey numbers** using a SAT solver  
- ✅ Perform **combinatorial bound analysis**  
- ✅ Visualize results and generate summary reports  

---

## Theoretical Background

> **Ramsey’s Theorem:**  
> For any positive integers \( r, s \), there exists a minimum number \( R(r, s) \) such that every red–blue coloring of the edges of a complete graph \( K_{R(r,s)} \) contains either a red \( K_r \) or a blue \( K_s \).

RamSat unites **three classical computational strategies**:

1. **Pigeonhole Principle Method**  
   Uses combinatorial arguments to estimate deterministic lower and upper bounds.

2. **Erdős Probabilistic Method**  
   Estimates Ramsey thresholds via random graph simulations and expected value arguments.

3. **SAT-Based Verification**  
   Encodes edge colorings into Boolean satisfiability problems and verifies the minimal \( n \) for which \( K_n \) satisfies Ramsey’s property.

---

## System Architecture

```text
+--------------------+
|   User Interface   |
+---------+----------+
          |
          v
+---------+----------+
|   Computation Core |
|  - PigeonholeCalc  |
|  - ErdosSimulator  |
|  - SATVerifier     |
+---------+----------+
          |
          v
+---------+----------+
| Visualization/Logs |
+--------------------+
```

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/RamSat.git
cd RamSat

# Create virtual environment (optional)
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt
```

## Usage
```bash
# Compute Ramsey number estimates using the Pigeonhole and Erdős methods
python main.py --r 3 --s 3

# Run SAT-based verification for small cases
python main.py --mode sat --r 4 --s 4

# Generate visualization of probabilistic simulations
python main.py --mode prob --r 5 --s 5 --plot
```

### Example Output
```bash
[+] Computing Ramsey Number R(3,3)
    > Pigeonhole Bound: 6 ≤ R(3,3) ≤ 7
    > Probabilistic Estimate: ~6.2
    > SAT Verification: R(3,3) = 6 ✅
```

## Tech Stack

| Component | Library / Tool | Purpose |
|------------|----------------|----------|
| **Programming Language** | Python 3.11+ | Core implementation |
| **SAT Solver** | PySAT / Z3 | Boolean satisfiability verification |
| **Math & Probability** | NumPy, SymPy | Combinatorial and probabilistic computations |
| **Visualization** | Matplotlib, Seaborn | Plotting and analysis |
| **Logging & Reporting** | Rich, Pandas | Pretty terminal logs and data tables |

---

## Example Visualization

**Example:** Probability distribution of colorings avoiding monochromatic triangles for \( K_n \).

<!-- ![Ramsey Distribution Example](assets/ramsey_plot_example.png) -->

---

## Research Applications

- Approximation of unknown Ramsey numbers  
- Combinatorial optimization and proof assistance  
- Probabilistic graph theory simulations  
- Verification via constraint satisfaction problems (CSPs)  
- Automated discovery of combinatorial limits  

---

## Future Work

- Extend support to **multi-color Ramsey numbers**  
- Add **GPU acceleration** for large probabilistic simulations  
- Integrate **machine learning models** for pattern-based bound prediction  
- Develop an **interactive web interface** for visual exploration  

---

## References

- F. P. Ramsey, *"On a Problem of Formal Logic"*, *Proceedings of the London Mathematical Society*, 1930  
- P. Erdős, *"Some remarks on the theory of graphs"*, *Bulletin of the AMS*, 1959  
- R. L. Graham, B. L. Rothschild, J. H. Spencer, *"Ramsey Theory"*, Wiley, 1990  
- V. Chvátal, *"A note on Ramsey numbers"*, *Journal of Combinatorial Theory*, 1970

## License

This project is licensed under the **MIT License**.  
See the [LICENSE](LICENSE) file for details.