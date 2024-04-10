from PIL import Image, ImageOps

from PIL import Image, ImageOps
from PIL import ImageFilter, ImageEnhance
import time


class TimeTake:
    def __init__(self):
        self.start_time = time.perf_counter()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = time.perf_counter()
        self.elapsed_time = self.end_time - self.start_time
        print(f"Time taken: {self.elapsed_time:.2f} seconds")

def simple_edge_detection(image, intensity):
    """
    Detects edges in an image using a simple edge detection algorithm.
    
    Args:
    - image (PIL.Image): The input image.
    - intensity (float): The intensity of the edge detection.

    Returns:
    - PIL.Image: The image with detected edges.
    """

    # Convert to grayscale
    gray_image = image.convert('L')
    
    # Enhance the contrast to make edges more distinguishable
    contrast_enhancer = ImageEnhance.Contrast(gray_image)
    high_contrast_image = contrast_enhancer.enhance(intensity)  # Factor 2.0 increases contrast
    
    # Apply an edge enhancement filter
    edge_enhanced_image = high_contrast_image.filter(ImageFilter.FIND_EDGES)
    
    return edge_enhanced_image

def edge_detect(image):
    """
    Detects edges in an image using a simple edge detection algorithm.
    
    Args:
    - image (PIL.Image): The input image.
    
    Returns:
    - PIL.Image: The image with detected edges.
    """
    # Convert the image to grayscale
    gray_image = ImageOps.grayscale(image)
    
    # Apply a simple edge detection filter and give the intensity of the edges
    edge_image = gray_image.filter(ImageFilter.FIND_EDGES)
    
    return edge_image

import numpy as np

def advanced_edge_detection(image_path):
    """
    Applies the Sobel operator for edge detection on an image using PIL and Numpy.
    
    Args:
    - image_path (str): Path to the input image.
    
    Returns:
    - Image: The image after applying the Sobel operator for edge detection.
    """
    # Open and convert the image to grayscale
    image = Image.open(image_path).convert('L')
    image_array = np.array(image)
    
    # Sobel kernels for edge detection
    sobel_kernel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    sobel_kernel_y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
    
    # Convolution function for applying kernels
    def convolve(image_array, kernel):
        kernel_height, kernel_width = kernel.shape
        image_height, image_width = image_array.shape
        output = np.zeros((image_height - kernel_height + 1, image_width - kernel_width + 1))
        
        for i in range(output.shape[0]):
            for j in range(output.shape[1]):
                output[i, j] = np.sum(image_array[i:i+kernel_height, j:j+kernel_width] * kernel)
        return output
    
    # Apply Sobel kernels
    gradient_x = convolve(image_array, sobel_kernel_x)
    gradient_y = convolve(image_array, sobel_kernel_y)
    
    # Calculate gradient magnitude
    gradient_magnitude = np.sqrt(gradient_x**2 + gradient_y**2)
    
    # Normalize to 0-255
    gradient_magnitude = (gradient_magnitude / gradient_magnitude.max()) * 255
    
    # Convert to image
    edge_image = Image.fromarray(gradient_magnitude.astype(np.uint8))
    
    return edge_image




# Commenting out the function call to prevent execution
if __name__ == "__main__":
    # Load an image
    image = Image.open("bb_000033.png")
    
    # Remove the black borders
    with TimeTake() as t:
        imag = simple_edge_detection("bb_000033.png")
    imag.save("edge_detection.png")

    with TimeTake() as t:
        imag2 = edge_detect(image)
    imag2.save("edge_detection2.png")

    with TimeTake() as t:
        imag3 = advanced_edge_detection("bb_000033.png")
    imag3.save("edge_detection3.png")