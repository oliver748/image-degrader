import os
from PIL import Image, ImageEnhance, UnidentifiedImageError
from PIL import ImageFilter, ImageOps
import numpy as np
import random
#from logger import Logger
from skimage.util import random_noise
from skimage.io import imsave
from skimage.transform import resize

class ImageManipulator:
    @staticmethod
    def open_image(image_path):
        """
        Open an image.
        :param image_path: str: The path to the image
        :return: Image: The opened image
        """
        try:
            image = Image.open(image_path)
        except UnidentifiedImageError:
            return None
        
        return image
    
    @staticmethod
    def saturate(image, value):
        """
        Saturate an image.
        :param value: float: The value to saturate the image
        """
        return ImageEnhance.Color(image).enhance(value)

    @staticmethod
    def brighten(image, value):
        """
        Brighten an image.
        :param value: float: The value to brighten the image
        """
        return ImageEnhance.Brightness(image).enhance(value)
    
    @staticmethod
    def contrast(image, value):
        """
        Change the contrast of an image.
        :param value: float: The value to change the contrast of the image
        """
        return ImageEnhance.Contrast(image).enhance(value)
    
    @staticmethod
    def sharpen(image, value):
        """
        Sharpen an image.
        :param value: float: The value to sharpen the image
        """
        return ImageEnhance.Sharpness(image).enhance(value)

    @staticmethod
    def simple_noise(image, intensity):
        """
        Apply a custom noise effect to an image using a faster method with NumPy.

        Parameters:
        - image_path: Path to the input image.
        - intensity: The intensity of the noise effect. Higher values produce more noticeable noise.

        Returns:
        - None. The function returns the modified image.
        """

        # Convert the image to a NumPy array
        img_array = np.array(image)
        
        # Generate noise
        noise = np.random.randint(-intensity, intensity + 1, img_array.shape, dtype='int16')
        
        # Add noise to the image
        img_array = img_array.astype('int16')  # Convert to int16 to prevent overflow
        img_array += noise
        img_array = np.clip(img_array, 0, 255)  # Ensure values stay in the 0-255 range
        
        # Convert back to an image
        return Image.fromarray(img_array.astype('uint8'))

    @staticmethod
    def complex_noise(image, intensity, mode):
        def gen_noise_mask(rows, cols, mode):
            # Full resolution
            noise_im1 = np.zeros((rows, cols))
            noise_im1 = random_noise(noise_im1, mode=mode, var=(intensity / 1000) ** 2, clip=False)

            # Half resolution
            noise_im2 = np.zeros((rows // 2, cols // 2))
            noise_im2 = random_noise(noise_im2, mode=mode, var=((intensity / 1000) * 2) ** 2, clip=False)
            noise_im2 = resize(noise_im2, (rows, cols))  # Upscale to original image size

            # Quarter resolution
            noise_im3 = np.zeros((rows // 4, cols // 4))
            noise_im3 = random_noise(noise_im3, mode=mode, var=((intensity / 1000) * 4) ** 2, clip=False)
            noise_im3 = resize(noise_im3, (rows, cols))  # What is the interpolation method?

            return noise_im1 + noise_im2 + noise_im3


        image_array = np.asarray(image)

        rows, cols, depth = image_array.shape

        rgba_array = np.zeros((rows, cols, depth), 'float64')
        for d in range(0, depth):
            rgba_array[..., d] += gen_noise_mask(rows, cols, mode)

        noisy_image = image_array / 255 + rgba_array  # Add noise_im to the input image.
        noisy_image = np.round((255 * noisy_image)).clip(0, 255).astype(np.uint8)

        return Image.fromarray(noisy_image)
    
    @staticmethod
    def resize(image, size):
        """
        Resize an image.
        :param size: tuple: The size to resize the image
        """
        return image.resize(size)

    @staticmethod
    def scale(image, scale):
        """
        Scale an image.
        :param scale: float: The scale to resize the image
        """
        width, height = image.size
        new_width = int(width * scale)
        new_height = int(height * scale)
        return image.resize((new_width, new_height))
    
    @staticmethod
    def rotate(image, angle, expand=False):
        """
        Rotate an image.
        :param angle: int: The angle to rotate the image
        :param crop: bool: Crop the image to the new size
        """
        return image.rotate(angle, expand=expand)
    
    @staticmethod
    def crop(image, box):
        """
        Crop an image.
        :param box: tuple: The box to crop the image
        """
        return image.crop(box)
    
    @staticmethod
    def remove_black_borders(image):
        """
        Remove black borders from an image.
        :param image: Image: The image to remove the black borders from
        """
        # Convert to grayscale to help with detecting the bounding box of the non-black area
        grayscale_image = ImageOps.grayscale(image)
        
        # Get the bounding box of the non-black area
        bbox = grayscale_image.getbbox()
        
        if bbox:
            # Crop the image to the bounding box to remove the black borders
            return image.crop(bbox)
        
        return image
    
    @staticmethod
    def blur(image, radius):
        """
        Blur an image.
        :param radius: float: The radius to blur the image
        """
        return image.filter(ImageFilter.GaussianBlur(radius))
    

    @staticmethod
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

    @staticmethod
    def save_image(image, output_path, quality):
        """
        Change the quality of an image.
        :param value: int: The value to change the quality of the image
        """
        # avoid "cannot write mode P as JPEG" error
        if output_path.endswith(".jpg") or output_path.endswith(".jpeg"):
            image = image.convert("RGB")

        return image.save(output_path, quality=quality)