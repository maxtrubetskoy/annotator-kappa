# Inter-Annotator Agreement for Medical Image Segmentation

This repository contains a Python script to measure the inter-annotator agreement for medical image segmentations. It calculates Cohen's Kappa and the F1-score for pairs of segmentations from different annotators (doctors).

## Directory Structure

The script expects the data to be organized in the following directory structure:

```
data/
├── doctor_id_1/
│   ├── patient_id_1/
│   │   └── segmentation/
│   │       └── segmentation.seg.nrrd
│   └── patient_id_2/
│       └── segmentation/
│           └── segmentation.seg.nrrd
├── doctor_id_2/
│   ├── patient_id_1/
│   │   └── segmentation/
│   │       └── segmentation.seg.nrrd
│   └── patient_id_3/
│       └── segmentation/
│           └── segmentation.seg.nrrd
└── ...
```

- `doctor_id`: A unique identifier for each annotator.
- `patient_id`: A unique identifier for each patient.
- `segmentation/`: A directory containing the segmentation file.
- `segmentation.seg.nrrd`: The segmentation file in `.seg.nrrd` format.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/annotator-kappa.git
    cd annotator-kappa
    ```

2.  **Install the required dependencies:**

    This project supports both `uv` and `pip` for dependency management. `uv` is recommended for faster performance.

    ### Using `uv` (Recommended)

    1.  **Install `uv`:**

        Follow the official instructions to install `uv` on your system. For example, on macOS and Linux:
        ```bash
        curl -LsSf https://astral.sh/uv/install.sh | sh
        ```

    2.  **Create a virtual environment and install dependencies:**

        `uv` can create a virtual environment and install the dependencies from `requirements.txt` in a single command:
        ```bash
        uv venv
        uv pip install -r requirements.txt
        ```

    3.  **Activate the virtual environment:**
        ```bash
        source .venv/bin/activate
        ```

    ### Using `pip`

    If you prefer to use `pip`, you can create a virtual environment and install the dependencies as follows:

    ```bash
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

## Usage

To run the script, use the following command:

```bash
python measure_agreement.py --data_dir /path/to/your/data
```

- `--data_dir`: The path to the root directory containing the data.
- `--output_file` (optional): The path to save the output CSV file. Defaults to `agreement_scores.csv`.

### Example

```bash
python measure_agreement.py --data_dir dummy_data --output_file results.csv
```

## Output

The script will generate a CSV file (e.g., `agreement_scores.csv`) with the following columns:

- `patient_id`: The ID of the patient.
- `doctor1`: The ID of the first doctor in the pair.
- `doctor2`: The ID of the second doctor in the pair.
- `cohen_kappa`: The Cohen's Kappa score for the pair of segmentations.
- `f1_score`: The F1-score for the pair of segmentations.

---

This project also includes a script to generate dummy data for testing purposes. You can run it as follows:

```bash
python create_dummy_data.py
```

This will create a `dummy_data` directory with the required structure and some sample `.seg.nrrd` files.
