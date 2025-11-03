# Implied Yields in Liquid Restaking: An Empirical Decomposition of Market-Implied Risk and Reward Premia

This repository contains the full source code, data, and analysis for the paper, "Implied Yields in Liquid Restaking: An Empirical Decomposition of Market-Implied Risk and Reward Premia."

## Overview

This research provides an empirical analysis of the market-implied yields for Liquid Restaking Tokens (LRTs). By using data from the yield derivatives protocol Pendle Finance, we construct the LRT Premium Spread (LPS) to isolate and measure the market's pricing of the unique risks and speculative rewards (e.g., points and airdrops) inherent in LRTs.

### Note on Previous Versions

This repository has been significantly refactored since the preliminary version of the paper. The code and data for the preliminary version of this work, presented at the *2025 IEEE International Workshop on Cryptocurrency Exchanges (CryptoEx)*, can be found by checking out the `v1.0-cryptoex2025` Git tag in the **Releases** section.

### Repository Structure

```project
├── new_data/
│   ├── benchmark/
│   │   └── ETH_styETH.csv
│   ├── tvl/
│   │   ├── bedrock uniETH.csv
│   │   ├── ether.fi.csv
│   │   └── ... (and other TVL files)
│   ├── ARB_Apr24_rsETH.csv
│   ├── ARB_Apr24_weETH.csv
│   └── ... (and other Pendle data files)
├── main.ipynb
├── README.md
├── requirements.txt
└── .gitignore
```

All data required for the analysis is located within the new_data/ directory.

1. Pendle Market Data:
   - The raw Pendle market data CSV files are located directly inside new_data/.
   - Files must be named in the format CHAIN_MONTHYEAR_ASSET.csv (e.g., ARB_Apr24_rsETH.csv). The notebook code parses these filenames to extract metadata.
   - Data can be updated by going on any pool on Pendle Finance and clicking the 'Download CSV' button: <https://www.pendle.finance>.
2. Protocol TVL Data:
    - TVL data is located in new_data/tvl/.
    - The notebook contains a function `fetch_all_tvl_data` which can be uncommented and run to automatically download the latest TVL data from the DeFiLlama API.
3. Benchmark Staking Rate Data:
    - The Compass STYETH Index data is located at new_data/benchmark/ETH_styETH.csv.
    - Data can be updated from the following source: <https://www.compassft.com/indice/styeth/>.

## Installation, Setup, and Reproducibility

The analysis was conducted in Python 3.11.7 within a Jupyter environment. Using a virtual environment (like Conda or venv) is strongly recommended for reproducing our setup.

1. Clone the repository

```bash
git clone https://github.com/farischaudhry/pendle-analysis.git
cd pendle-analysis
```

2. Install dependencies

The required Python libraries are listed in requirements.txt. Install them using pip after entering the conda/venv:

```bash
pip install uv
pip install -r requirements.txt
```

3. Run Notebook

To reproduce the full analysis and generate all figures from the paper, follow these steps.

- Open the `main.ipynb` notebook on e.g., Visual Studio Code.
- Select the interpeter to be the version of python/venv/conda environment that the dependencies were installed into.
- To run the full analysis, you can either execute all cells sequentially ("Run All") or step through each cell individually.
- The notebook will generate all plots and statistical outputs inline. These outputs correspond directly to the figures and results presented in the manuscript.

## Citation

If you use the code, data, or findings from this research in your own work, please cite the original paper:

```bibtex
@misc{chaudhry2025pendle,
  author = {Chaudhry, Faris},
  title = {Implied Yields in Liquid Restaking: An Empirical Decomposition of Market-Implied Risk and Reward Premia},
  year = {2025},
  publisher = {Research Square},
  doi = {10.21203/rs.3.rs-7411925/v1},
  url = {https://doi.org/10.21203/rs.3.rs-7411925/v1},
  note = {Preprint}
}
```
