from fastapi import APIRouter, HTTPException
import base64
from io import BytesIO
from apps.calculator.utils import analyze_image
from schema import ImageData
from PIL import Image

router = APIRouter()

@router.post('')
async def run(data: ImageData):
    try:
        # Decode base64 image data
        image_data = base64.b64decode(data.image.split(",")[1])  # Assumes data:image/png;base64,<data>
        image_bytes = BytesIO(image_data)
        image = Image.open(image_bytes)

        # Analyze the image
        responses = analyze_image(image, dict_of_vars=data.dict_of_vars)
        
        # Ensure responses are returned in the correct format
        if not isinstance(responses, list):
            raise ValueError("Invalid response format: Expected list of responses.")

        # Prepare the response data
        data = []
        for response in responses:
            # Check if response contains the required fields
            if "result" not in response or "expr" not in response:
                raise ValueError("Missing 'result' or 'expr' in response.")

            data.append(response)

        return {"message": "Image processed", "data": data, "status": "success"}

    except Exception as e:
        # Log the error
        print(f"Error processing image: {e}")

        # Return a detailed error response with a 400 status code
        raise HTTPException(status_code=400, detail=f"Error processing the image: {str(e)}")
