import argparse
from pathlib import Path

import mlflow
import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets, models, transforms


# MLflow setup
mlflow.set_tracking_uri("http://127.0.0.1:5000")
mlflow.set_experiment("food11")


# Command-line arguments
parser = argparse.ArgumentParser()

parser.add_argument("--dataset", choices=["mini", "processed"], default="mini")
parser.add_argument("--epochs", type=int, default=5)
parser.add_argument("--lr", type=float, default=0.001)
parser.add_argument("--batch-size", type=int, default=32)

args = parser.parse_args()


# Dataset paths
BASE_DIR = Path(__file__).resolve().parents[2]

if args.dataset == "mini":
    DATA_DIR = BASE_DIR / "data" / "food11_processed_mini"
else:
    DATA_DIR = BASE_DIR / "data" / "food11_processed"


# Image transformation
transform = transforms.Compose([
    transforms.ToTensor(),
])


# Load datasets
train_dataset = datasets.ImageFolder(
    DATA_DIR / "training",
    transform=transform
)

val_dataset = datasets.ImageFolder(
    DATA_DIR / "validation",
    transform=transform
)

test_dataset = datasets.ImageFolder(
    DATA_DIR / "evaluation",
    transform=transform
)


# Data loaders
train_loader = DataLoader(
    train_dataset,
    batch_size=args.batch_size,
    shuffle=True
)

val_loader = DataLoader(
    val_dataset,
    batch_size=args.batch_size,
    shuffle=False
)

test_loader = DataLoader(
    test_dataset,
    batch_size=args.batch_size,
    shuffle=False
)


# ResNet18 model
model = models.resnet18(
    weights=models.ResNet18_Weights.DEFAULT
)

# Food-11 has 11 classes
model.fc = nn.Linear(model.fc.in_features, 11)


# Device
device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

model = model.to(device)


# Loss and optimizer
criterion = nn.CrossEntropyLoss()

optimizer = torch.optim.Adam(
    model.parameters(),
    lr=args.lr
)


# Start MLflow run
with mlflow.start_run():

    # Log hyperparameters
    mlflow.log_params({
        "dataset": args.dataset,
        "epochs": args.epochs,
        "lr": args.lr,
        "batch_size": args.batch_size,
    })


    # Training
    for epoch in range(args.epochs):

        model.train()
        running_loss = 0.0

        for images, labels in train_loader:

            images = images.to(device)
            labels = labels.to(device)

            optimizer.zero_grad()

            outputs = model(images)

            loss = criterion(outputs, labels)

            loss.backward()
            optimizer.step()

            running_loss += loss.item()

        train_loss = running_loss / len(train_loader)


        # Validation
        model.eval()

        val_loss = 0.0
        correct = 0
        total = 0

        with torch.no_grad():

            for images, labels in val_loader:

                images = images.to(device)
                labels = labels.to(device)

                outputs = model(images)

                loss = criterion(outputs, labels)

                val_loss += loss.item()

                _, predicted = torch.max(outputs, 1)

                total += labels.size(0)
                correct += (predicted == labels).sum().item()

        val_loss = val_loss / len(val_loader)
        val_accuracy = correct / total


        # Log metrics for this epoch
        mlflow.log_metric(
            "train_loss",
            train_loss,
            step=epoch
        )

        mlflow.log_metric(
            "val_loss",
            val_loss,
            step=epoch
        )

        mlflow.log_metric(
            "val_accuracy",
            val_accuracy,
            step=epoch
        )


        # Show epoch results
        print(
            f"Epoch {epoch + 1}/{args.epochs} "
            f"- train_loss: {train_loss:.4f} "
            f"- val_loss: {val_loss:.4f} "
            f"- val_accuracy: {val_accuracy:.4f}"
        )


    # Test the final model
    model.eval()

    correct = 0
    total = 0

    with torch.no_grad():

        for images, labels in test_loader:

            images = images.to(device)
            labels = labels.to(device)

            outputs = model(images)

            _, predicted = torch.max(outputs, 1)

            total += labels.size(0)
            correct += (predicted == labels).sum().item()


    # Final test accuracy
    test_accuracy = correct / total

    mlflow.log_metric(
        "test_accuracy",
        test_accuracy
    )


    # Example input needed by MLflow when saving the model
    input_example = torch.randn(
        1, 3, 128, 128
    ).to(device)


    # Save trained model in MLflow
    mlflow.pytorch.log_model(
        model,
        name="model",
        input_example=input_example,
        serialization_format="pickle"
    )


    print(
        f"Final test accuracy: {test_accuracy:.4f}"
    )