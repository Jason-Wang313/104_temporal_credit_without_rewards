# Hostile Prior Work

The closest threats are methods that already extract training signal across time, handle delayed or sparse feedback, or diagnose causal mistakes in imitation and sequence models.

- RUDDER assigns credit in reinforcement learning with delayed rewards.
- Hindsight Experience Replay relabels sparse outcomes into useful training signal.
- Decision Transformer and return-conditioned sequence models use long-horizon context and return information.
- Causal confusion in imitation learning shows that policies can exploit spurious temporal correlates.
- Attention-is-explanation critiques warn that attention weights alone are not causal credit.
- Long-horizon robot learning methods already decompose tasks into stages or relays.

The v4 novelty boundary is therefore narrow: Paper 104 is not "do credit assignment" and not "add a pseudo reward." It must show reward-free temporal credit from physical event structure when scalar rewards are absent and temporal confounding hides the action that caused success or failure.

Current evidence supports this boundary locally, but real robot or independent high-fidelity validation remains required.
