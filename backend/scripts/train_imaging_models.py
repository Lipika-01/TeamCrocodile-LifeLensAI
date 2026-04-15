import os
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.layers import Dense, Flatten, Dropout, GlobalAveragePooling2D
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from sklearn.metrics import classification_report, confusion_matrix
import glob

# Project Root Resolution (Ensures script runs from backend root context)
BACKEND_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(BACKEND_ROOT)

def get_path(rel_path):
    # Try backend root first, then project root
    b_path = os.path.join(BACKEND_ROOT, rel_path)
    if os.path.exists(b_path) or not os.path.exists(os.path.join(PROJECT_ROOT, rel_path)):
        return b_path
    return os.path.join(PROJECT_ROOT, rel_path)

BREAST_MODEL_PATH = get_path("models/breast_cancer_model.h5")
BRAIN_MODEL_PATH = get_path("models/brain_tumor_model.h5")

# Ensure models directory exists
os.makedirs(get_path("models"), exist_ok=True)

def train_breast_cancer_model():
    print("\n--- Training Breast Cancer Model (CBIS-DDSM) ---")
    csv_path = "datasets/breast cancer/csv/mass_case_description_train_set.csv"
    jpeg_root = "datasets/breast cancer/jpeg/"
    
    if not os.path.exists(csv_path):
        print(f"Error: CSV not found at {csv_path}")
        return

    df = pd.read_csv(csv_path)
    # Filter only mass and relevant pathology
    df = df[df['abnormality type'] == 'mass']
    df = df[df['pathology'].isin(['BENIGN', 'MALIGNANT'])]
    
    # Randomly sample for speed as requested
    df = df.sample(n=min(len(df), 3000), random_state=42)
    
    # Path Mapping Logic
    # CSV Path: Mass-Training_.../UID2/UID3/000000.dcm
    # JPEG Folder name: UID2
    def map_path(x):
        parts = x.split('/')
        if len(parts) > 2:
            series_uid = parts[2]
            folder_path = os.path.join(jpeg_root, series_uid)
            if os.path.exists(folder_path):
                # Search for any jpg in subfolders
                for r, d, f in os.walk(folder_path):
                    for file in f:
                        if file.lower().endswith('.jpg'):
                            return os.path.join(r, file)
        return None

    df['actual_path'] = df['image file path'].apply(map_path)
    df = df.dropna(subset=['actual_path'])
    
    # Label encoding
    df['label'] = df['pathology'].apply(lambda x: '1' if x == 'MALIGNANT' else '0')
    
    print(f"Dataset Size: {len(df)}")
    
    datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        width_shift_range=0.1,
        height_shift_range=0.1,
        zoom_range=0.2,
        horizontal_flip=True,
        validation_split=0.2
    )
    
    train_gen = datagen.flow_from_dataframe(
        df,
        x_col='actual_path',
        y_col='label',
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='binary',
        subset='training'
    )
    
    val_gen = datagen.flow_from_dataframe(
        df,
        x_col='actual_path',
        y_col='label',
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='binary',
        subset='validation'
    )
    
    # Model Setup
    base_model = ResNet50(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
    base_model.trainable = False
    
    x = Flatten()(base_model.output)
    x = Dense(128, activation='relu')(x)
    x = Dropout(0.5)(x)
    output = Dense(1, activation='sigmoid')(x)
    
    model = Model(inputs=base_model.input, outputs=output)
    model.compile(optimizer=Adam(learning_rate=0.0001), loss='binary_crossentropy', metrics=['accuracy'])
    
    model.fit(train_gen, validation_data=val_gen, epochs=5)
    model.save(BREAST_MODEL_PATH)
    print(f"Model saved to {BREAST_MODEL_PATH}")

def train_brain_tumor_model():
    print("\n--- Training Brain Tumor Model (MRI) ---")
    train_dir = "datasets/brain tumor/Training"
    test_dir = "datasets/brain tumor/Testing"
    
    if not os.path.exists(train_dir):
        print(f"Error: Training directory not found at {train_dir}")
        return

    datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        zoom_range=0.2,
        horizontal_flip=True,
        validation_split=0.2
    )
    
    train_gen = datagen.flow_from_directory(
        train_dir,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='training'
    )
    
    val_gen = datagen.flow_from_directory(
        train_dir,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='validation'
    )
    
    # Model Setup
    base_model = ResNet50(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
    base_model.trainable = False
    
    x = GlobalAveragePooling2D()(base_model.output)
    x = Dense(128, activation='relu')(x)
    x = Dropout(0.5)(x)
    output = Dense(train_gen.num_classes, activation='softmax')(x)
    
    model = Model(inputs=base_model.input, outputs=output)
    model.compile(optimizer=Adam(learning_rate=0.0001), loss='categorical_crossentropy', metrics=['accuracy'])
    
    model.fit(train_gen, validation_data=val_gen, epochs=5)
    model.save(BRAIN_MODEL_PATH)
    print(f"Model saved to {BRAIN_MODEL_PATH}")
    print(f"Classes: {train_gen.class_indices}")

if __name__ == "__main__":
    train_breast_cancer_model()
    train_brain_tumor_model()
