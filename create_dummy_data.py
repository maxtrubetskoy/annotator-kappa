import os
import numpy as np
import nrrd

def create_dummy_data(base_dir='dummy_data', num_doctors=3, num_patients=3):
    """
    Creates a dummy data directory structure with dummy .seg.nrrd files.
    """
    if os.path.exists(base_dir):
        print(f"Directory '{base_dir}' already exists. Skipping creation.")
        return

    os.makedirs(base_dir, exist_ok=True)
    print(f"Created base directory: {base_dir}")

    for i in range(1, num_doctors + 1):
        doctor_id = f'doctor{i}'
        doctor_dir = os.path.join(base_dir, doctor_id)
        os.makedirs(doctor_dir, exist_ok=True)

        for j in range(1, num_patients + 1):
            # Not all doctors have segmented all patients
            if np.random.rand() > 0.3:
                patient_id = f'patient{j}'
                patient_dir = os.path.join(doctor_dir, patient_id, 'segmentation')
                os.makedirs(patient_dir, exist_ok=True)

                # Create a dummy segmentation file
                # The segmentation is a 10x10x10 cube with a sphere of 1s
                data = np.zeros((10, 10, 10), dtype=np.uint8)
                x, y, z = np.ogrid[-4:6, -4:6, -4:6]
                mask = x*x + y*y + z*z <= 3*3
                # Add some noise to make segmentations different
                noise = np.random.randint(0, 2, size=(10, 10, 10), dtype=np.uint8)
                data[mask] = 1
                data = (data + noise) % 2


                # Save the dummy segmentation file
                segmentation_file = os.path.join(patient_dir, 'segmentation.seg.nrrd')
                nrrd.write(segmentation_file, data)
                print(f"Created dummy file: {segmentation_file}")

if __name__ == '__main__':
    create_dummy_data()
