#!/bin/bash
echo "🚀 TESTING ALL REAL DATASETS FROM HUGGING FACE"
echo "================================================"

echo -e "\n1️⃣ Testing all 5 datasets..."
python test_real_datasets.py

echo -e "\n2️⃣ Testing dataset switching..."
python test_dataset_switch.py

echo -e "\n🎉 ALL TESTS COMPLETE!"
