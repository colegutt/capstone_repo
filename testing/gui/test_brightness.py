import os
import time

try:
    while True:
        for gamma in [1.0, 1.2, 1.5, 1.8, 2.0]:  # Adjust gamma values as needed
            print(gamma)
            os.system(f"xgamma -gamma {gamma}")
            time.sleep(1)  # Wait for 2 seconds
except KeyboardInterrupt:
    os.system(f"xgamma -gamma {1.0}")