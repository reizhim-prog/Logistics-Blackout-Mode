# Logistics-Blackout-Mode
Logistics Blackout Mode (LBM) is an offline decision support tool for disaster response. It prioritizes affected areas during the first 72 hours using pre-disaster data and a multi-criteria scoring model, enabling fast and transparent logistics decisions under information blackout.
It helps prioritize affected areas during the first 72 hours after a disaster, when real-time data, electricity, and communication networks are often unavailable.

The system uses pre-disaster spatial data and a multi-criteria decision-making model (Simple Additive Weighting) to generate transparent and explainable priority rankings for emergency logistics distribution.

Key Features
Works fully offline (local web app)
Prioritization based on hazard, population exposure, and healthcare accessibility
Transparent scoring and explainable outputs
Designed for information blackout scenarios
Exportable results (CSV)

Use Case
LBM is intended to support emergency operation centers as a baseline decision tool, not as a predictive system.
It provides conservative but operationally useful recommendations for rapid logistics planning under severe uncertainty.

Methodology
The system applies:
Haversine distance for spatial calculations
Min-max normalization
Simple Additive Weighting (MCDM)
Disclaimer

LBM is not a disaster prediction system.
It is a decision support framework for early response under limited information.
