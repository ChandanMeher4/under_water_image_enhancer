# main.py

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from PIL import Image
import io
import os

# Import your existing Predictor class
from predict import Predictor

# --- Application Setup ---
# Create directories if they don't exist
os.makedirs('uploads', exist_ok=True)
os.makedirs('outputs', exist_ok=True)

# Define the path to your trained model
MODEL_PATH = 'checkpoints/best_model.pth'

# Initialize the Predictor
# This will load your UNet model and weights
predictor = None
if os.path.exists(MODEL_PATH):
    print(f"Loading model from {MODEL_PATH}...")
    predictor = Predictor(MODEL_PATH)
    print("Model loaded successfully!")
else:
    print(f"ERROR: Model not found at {MODEL_PATH}. The API will not work.")
    # In a real application, you might want to prevent the app from starting
    # if the model can't be loaded.

# --- FastAPI App ---
app = FastAPI(
    title="Underwater Image Enhancer API",
    description="An API that uses a U-Net model to enhance underwater images.",
    version="1.0"
)

@app.get("/", summary="Root Endpoint")
def read_root():
    """A simple endpoint to check if the API is running."""
    return {"message": "Welcome to the Underwater Image Enhancer API!"}


@app.post(
    "/enhance-image/",
    summary="Enhance an underwater image",
    description="Upload an image file (PNG, JPG, JPEG, BMP) to be enhanced by the U-Net model."
)
async def enhance_image(file: UploadFile = File(...)):
    """
    This endpoint takes an uploaded image, saves it temporarily,
    runs the enhancement model on it, and returns the enhanced image.
    """
    if predictor is None:
        raise HTTPException(status_code=503, detail="Model is not available. Please check server logs.")

    # Validate file type
    allowed_extensions = {'png', 'jpg', 'jpeg', 'bmp'}
    extension = file.filename.split('.')[-1].lower()
    if extension not in allowed_extensions:
        raise HTTPException(status_code=400, detail=f"Invalid file type. Allowed types are: {allowed_extensions}")

    try:
        # Define paths for temporary storage
        input_path = os.path.join('uploads', file.filename)
        output_filename = f"enhanced_{file.filename}"
        output_path = os.path.join('outputs', output_filename)

        # Save the uploaded file
        with open(input_path, "wb") as buffer:
            buffer.write(await file.read())

        # Use your existing predictor to process the image
        # The predict method saves the output to output_path
        predictor.predict(input_path, output_path)

        # Open the enhanced image and return it as a response
        with open(output_path, "rb") as enhanced_file:
            enhanced_image_bytes = enhanced_file.read()

        # Clean up the temporary files
        os.remove(input_path)
        os.remove(output_path)
        
        # Return the enhanced image bytes
        return StreamingResponse(io.BytesIO(enhanced_image_bytes), media_type=f"image/{extension}")

    except Exception as e:
        # If anything goes wrong, return an error
        raise HTTPException(status_code=500, detail=f"An error occurred during processing: {str(e)}")