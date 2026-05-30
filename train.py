import argparse
import pickle
from pathlib import Path
from src.main.data.loader import load_data, preprocess_training_data
from src.main.features.engine import extract_date_features
from src.main.models.predictor import DelayPredictor

def main():
    parser = argparse.ArgumentParser(description="Train the Invoice Delay Prediction Model")
    parser.add_argument("--data", type=str, default="1806126.csv", help="Path to training data CSV")
    parser.add_argument("--output", type=str, default="model.pkl", help="Path to save the trained model")
    
    args = parser.parse_args()
    
    csv_path = Path(args.data)
    output_path = Path(args.output)
    
    print(f"Loading data from {csv_path}...")
    df = load_data(csv_path)
    
    print("Preprocessing data...")
    train_df = preprocess_training_data(df)
    train_df = extract_date_features(train_df)
    
    print("Training model...")
    predictor = DelayPredictor()
    predictor.train(train_df)
    
    print(f"Saving model to {output_path}...")
    with open(output_path, "wb") as f:
        pickle.dump(predictor, f)
    
    print("Done!")

if __name__ == "__main__":
    main()
