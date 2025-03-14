# Model Directory

This directory is used to store machine learning models for the Food IQ application.

## Required Models

### Indian Food CNN Model

Place your TensorFlow model file here with the name `Indian_Food_CNN_Model.h5`.

The model should be trained to recognize the following food classes:
```
aloo_matar, appam, bhindi_masala, biryani, butter_chicken,
chapati, chicken_tikka, chole_bhature, daal_baati_churma,
daal_puri, dal_makhani, dhokla, gulab_jamun, idli, jalebi,
kaathi_rolls, kadai_paneer, masala_dosa, mysore_pak, pakode,
palak_paneer, paneer_butter_masala, paani_puri, pav_bhaji, samosa
```

## Model Format

The model should be a TensorFlow/Keras model saved in the H5 format with the following specifications:

- Input shape: (None, 224, 224, 3) - RGB images of size 224x224
- Output shape: (None, 25) - Probabilities for the 25 food classes

## Testing Your Model

After placing the model file in this directory, you can test it by:

1. Starting the API server: `uvicorn main:app --reload`
2. Uploading an image to the `/image/predict` endpoint

The API will return the predicted food class and confidence score. 