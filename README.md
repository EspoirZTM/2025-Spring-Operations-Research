# 2025 Spring Operations Research Assignment Solutions

This repository contains solutions to three operations research problems developed for the 2025 Spring Operations Research course. The solutions include theoretical modeling, numerical analysis, and practical implementations using Python. All core code is available in this repository, ensuring reproducibility and further exploration.

---

## Chapter 1: Three Cowboys Game Problem

### Overview
This problem models a simultaneous duel among three cowboys—Jack (80% accuracy), John (60% accuracy), and Carter (40% accuracy)—using a Markov decision process. Each cowboy acts rationally to maximize survival, leading to a counterintuitive "weakest player advantage" phenomenon.

### Key Findings
- **Model**: A Markov chain with 7 states (including absorption states) was constructed.  
- **Results**: After convergence (by ~10 rounds), Carter has the highest survival probability (~82.4%), while Jack and John have significantly lower probabilities (~1.8% and ~3.4%, respectively).  
- **Insight**: The weakest player (Carter) benefits from being overlooked in initial targeting, while stronger players become primary threats.  

Visualization of the state transitions:  
[](@replace=1)


---

## Chapter 2: Book Sales Agent Location Problem

### Overview
A facility location problem aimed at maximizing student coverage across 7 districts by strategically placing 2 book sales agents. Each agent serves its home district and one adjacent district.

### Key Findings
- **Model**: An integer linear programming (ILP) formulation based on the Maximum Covering Location Problem (MCLP).  
- **Optimal Solution**: Agents placed in **District 2** (covering District 5) and **District 7** (covering District 4), achieving coverage of **177,000 students**.  
- **Methodology**: Used combinatorial enumeration to evaluate all feasible pairs, ensuring global optimality.  

Illustration of the optimal coverage:  
[](@replace=2)


---

## Chapter 3: Designing a Chaotic System

### Overview
A custom chaotic system (Zhu-Chaos) was designed by augmenting the classic Rössler system with coupling terms and periodic perturbations. The system's stability was analyzed using Lyapunov theory.

### Key Findings
- **System Dynamics**:
- 
ẋ = -y - z + α⋅sin(z)  
ẏ = x + a⋅y  
ż = b + z(x - c) + β⋅cos(x)

- **Stability Conditions**:  
  - Local asymptotic stability: $a < 0$ and $c > 0$.  
  - Global exponential stability: Additional $\alpha < 1$ and $c > \frac{\beta}{2}$.  
- **Validation**: Numerical simulations confirm chaotic behavior under parameter variations.  

Phase portrait visualization:  
[](@replace=3)


---

## Code Implementation
All solutions are implemented in Python, with core code provided in the `src` directory:
- **Cowboy Duel Simulator**: Computes survival probabilities using Markov chain transitions (`cowboy_game.py`).  
- **Agent Location Solver**: Uses combinatorial search to optimize coverage (`location_model.py`).  
- **Chaos System Simulator**: Integrates the Zhu-Chaos equations and generates visualizations (`chaos_system.py`).  

Explore the code to replicate results or extend the models. Contributions are welcome!

---

**Note**: This README summarizes the assignment. Full details, including LaTeX sources and additional figures, are in the repository. Clone or fork to dive deeper into the analysis!
