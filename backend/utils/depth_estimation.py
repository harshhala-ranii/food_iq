import torch
import torch.nn.functional as F
import numpy as np
import cv2
from PIL import Image
import logging
import os

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Device setup
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
logger.info(f"Using device: {device}")

# Load MiDaS model and transforms
try:
    midas_model = torch.hub.load("intel-isl/MiDaS", "DPT_Large")
    midas_model.to(device)
    midas_model.eval()
    midas_transforms = torch.hub.load("intel-isl/MiDaS", "transforms")
    transform = midas_transforms.dpt_transform
except Exception as e:
    logger.error(f"Model init failed: {e}")
    raise

def estimate_depth(image: Image.Image) -> np.ndarray:
    """
    Estimate relative depth map using MiDaS.
    """
    try:
        img = np.array(image.convert("RGB"))
        img_resized = cv2.resize(img, (640, 480))

        input_tensor = transform(img_resized).to(device)

        with torch.no_grad():
            prediction = midas_model(input_tensor)
            prediction = F.interpolate(
                prediction.unsqueeze(1),
                size=img_resized.shape[:2],
                mode="bicubic",
                align_corners=False
            ).squeeze()

        return prediction.cpu().numpy()
    except Exception as e:
        logger.error(f"Depth estimation error: {e}")
        raise

def create_mask(image: Image.Image) -> np.ndarray:
    """
    Create binary mask using grayscale thresholding.
    """
    try:
        img = np.asarray(image.convert("RGB"))
        img_resized = cv2.resize(img, (640, 480))

        gray = cv2.cvtColor(img_resized, cv2.COLOR_RGB2GRAY)
        _, mask = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

        return mask.astype(np.uint8)
    except Exception as e:
        logger.error(f"Mask creation error: {e}")
        raise

def estimate_volume_from_depth(depth_map: np.ndarray, mask: np.ndarray, reference_volume_ml: float = 240.0) -> float:
    """
    Estimate relative volume in ml from masked depth.
    """
    try:
        masked_depth = np.where(mask == 255, depth_map, 0)

        max_depth = np.max(masked_depth)
        if max_depth <= 0:
            logger.warning("No valid depth found under mask.")
            return 0.0

        normalized_depth = masked_depth / max_depth
        relative_volume = np.sum(normalized_depth)

        pixel_count = np.sum(mask == 255)
        if pixel_count == 0:
            logger.warning("Empty mask detected.")
            return 0.0

        volume_ml = (relative_volume / pixel_count) * reference_volume_ml
        return round(float(volume_ml), 2)

    except Exception as e:
        logger.error(f"Volume estimation error: {e}")
        raise

def generate_masked_image(image: Image.Image, mask: np.ndarray) -> Image.Image:
    """
    Generate masked overlay visualization.
    """
    try:
        img_array = np.array(image.convert("RGB"))
        img_array = cv2.resize(img_array, (mask.shape[1], mask.shape[0]))

        overlay = np.zeros_like(img_array)
        overlay[mask == 255] = [0, 255, 0]

        blended = cv2.addWeighted(img_array, 1, overlay, 0.3, 0)
        return Image.fromarray(blended)
    except Exception as e:
        logger.error(f"Masked image visualization error: {e}")
        raise

def run_pipeline(image_path: str):
    """
    Run full food volume estimation pipeline.
    """
    try:
        image = Image.open(image_path)
        logger.info("Estimating depth...")
        depth = estimate_depth(image)

        logger.info("Creating mask...")
        mask = create_mask(image)

        logger.info("Estimating volume...")
        volume = estimate_volume_from_depth(depth, mask)

        logger.info(f"✅ Estimated Volume: {volume} ml")

        logger.info("Saving masked overlay image...")
        vis_image = generate_masked_image(image, mask)
        vis_image.save("masked_output.png")
        logger.info("Saved as 'masked_output.png'")

    except Exception as e:
        logger.error(f"Pipeline failed: {e}")

