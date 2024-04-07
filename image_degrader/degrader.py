""""""""""""

import sys
sys.path.append("image_degrader")

import os
import utils.logger as logg
import utils.file_handler as file_handler
import utils.image_manipulator as image_manipulator
from PIL import Image, ImageEnhance
import random


class ImageDegrader:
    """
    Degrade images by applying different filters, effects etc.
    """

    def __init__(self):
        self.logger = logg.Logger("ImageDegrader", logg.logging.DEBUG)
        self.file_handler = file_handler.FileHandler()
        self.im = image_manipulator.ImageManipulator()


        # self.images_dir = images_dir
        # self.image_files = self.file_handler.get_images(dir_path=images_dir) if images_dir else None
        # self.image_path = image_path if image_path else None

        # self.verify_env()

    # def verify_env(self):
    #     if self.image_files is None and self.image_path is None:
    #         raise ValueError("Please provide either an images directory or an image path.")
        
    #     if self.image_files is not None and self.image_path is not None:
    #         raise ValueError("Please provide either an images directory or an image path, not both.")
        
    #     # check the path
    #     # TODO: Måske ikke nødvendig, burde tjekkes
    #     if self.image_files:
    #         if not self.file_handler.verify_path(self.images_dir):
    #             raise FileNotFoundError(f"Folder path \"{self.images_dir}\" not found.")
            
    #     if self.image_path:
    #         if not self.file_handler.verify_path(self.image_path):
    #             raise FileNotFoundError(f"Image path \"{self.image_path}\" not found.")
    

    
    def degrade_image(
            self,
            image_path,
            mode="single",
            output_dir="result",
            output_format="jpeg",
            saturation=None,
            brightness=None,
            contrast=None,
            sharpness=None,
            noise=None,
            quality=100,
        ):

        # check its path
        if not self.file_handler.verify_path(image_path):
            self.logger.error(f"Image at path \"{image_path}\" not found.")
            return

        if mode == "single":
            os.makedirs(output_dir, exist_ok=True)

        self.logger.info(f"Processing image: \"{image_path}\"")
        image = self.im.open_image(image_path)
        
        # if image is invalid
        if image is None:
            self.logger.error(f"Image at path \"{image_path}\" could not be processed.")
            return

        if saturation:
            image = self.im.saturate(image, saturation)
        
        if brightness:
            image = self.im.brighten(image, brightness)
        
        if contrast:
            image = self.im.contrast(image, contrast)
        
        if sharpness:
            image = self.im.sharpen(image, sharpness)
        
        if noise:
            image = self.im.apply_noise(image, noise)
        
        #self.im.save_image(image, output_dir, os., output_format, quality)
        self.im.save_image(image, output_dir, os.path.basename(image_path), output_format, quality)
        self.logger.info(f"Image saved to \"{output_dir}\"")
        

        


    def batch_degrade_images(
            self,
            input_dir,
            output_dir="result",
            output_format="jpeg",
            saturation=None,
            brightness=None,
            contrast=None,
            sharpness=None,
            noise=50,
            quality=100,
        ):
        # check the input dir path
        if not self.file_handler.verify_path(input_dir):
            raise FileNotFoundError(f"Folder path \"{input_dir}\" not found.")
            return
        
        os.makedirs(output_dir, exist_ok=True)

        for image_path in self.image_files:
            self.logger.info(f"Processing image: \"{image_path}\"")
            self.degrade_image(
                image_path,
                mode="batch",
                output_dir=output_dir,
                output_format=output_format,
                saturation=saturation,
                brightness=brightness,
                contrast=contrast,
                sharpness=sharpness,
                noise=noise,
                quality=quality
            )