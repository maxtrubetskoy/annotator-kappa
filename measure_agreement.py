import os
import argparse
import nrrd
import numpy as np
import pandas as pd
from sklearn.metrics import cohen_kappa_score, f1_score
from itertools import combinations
import warnings

# Suppress pandas performance warning
warnings.simplefilter(action='ignore', category=pd.errors.PerformanceWarning)


def find_segmentations(data_dir):
    """
    Finds all segmentation files and groups them by patient.
    """
    patients = {}
    for doctor_id in os.listdir(data_dir):
        doctor_dir = os.path.join(data_dir, doctor_id)
        if not os.path.isdir(doctor_dir):
            continue

        for patient_id in os.listdir(doctor_dir):
            patient_dir = os.path.join(doctor_dir, patient_id)
            segmentation_dir = os.path.join(patient_dir, 'segmentation')
            if not os.path.isdir(segmentation_dir):
                continue

            for filename in os.listdir(segmentation_dir):
                if filename.endswith('.seg.nrrd'):
                    filepath = os.path.join(segmentation_dir, filename)
                    if patient_id not in patients:
                        patients[patient_id] = []
                    patients[patient_id].append({
                        'doctor': doctor_id,
                        'path': filepath
                    })
    return patients

def calculate_agreement(patients):
    """
    Calculates inter-annotator agreement for each patient.
    """
    results = []
    for patient_id, annotations in patients.items():
        if len(annotations) < 2:
            continue

        for (anno1, anno2) in combinations(annotations, 2):
            try:
                # Read segmentation files
                # print(f"comparing {anno1['path']} and {anno2['path']}")
                data1, _ = nrrd.read(anno1['path'])
                data2, _ = nrrd.read(anno2['path'])

                # Flatten the arrays for metric calculation
                flat_data1 = data1.flatten()
                flat_data2 = data2.flatten()
                flat_data1[flat_data1 > 0] = 1.0
                flat_data2[flat_data2 > 0] = 1.0
                # Calculate metrics
                kappa = cohen_kappa_score(flat_data1, flat_data2)
                f1 = f1_score(flat_data1, flat_data2, average='binary')

                results.append({
                    'patient_id': patient_id,
                    'doctor1': anno1['doctor'],
                    'doctor2': anno2['doctor'],
                    'cohen_kappa': kappa,
                    'f1_score': f1
                })
            except Exception as e:
                print(f"Could not process pair for patient {patient_id} ({anno1['doctor']}, {anno2['doctor']}): {e}")

    return results

def main():
    parser = argparse.ArgumentParser(description="Measure inter-annotator agreement for segmentations.")
    parser.add_argument('--data_dir', type=str, required=True, help="Path to the data directory.")
    parser.add_argument('--output_file', type=str, default='agreement_scores.csv', help="Path to the output CSV file.")
    args = parser.parse_args()

    patients = find_segmentations(args.data_dir)
    results = calculate_agreement(patients)

    if results:
        df = pd.DataFrame(results)
        df.to_csv(args.output_file, index=False)
        print(f"Results saved to {args.output_file}")
    else:
        print("No pairs found to compare.")

if __name__ == '__main__':
    main()
