""""""""""""

import sys
sys.path.append("image_degrader")

import os
import utils.logger as logger
import utils.file_handler as file_handler
import utils.image_manipulator as image_manipulator
import utils.time_take as time_take

class ImageDegrader:
    def __init__(self, debug=False):
        self.logger = logger.Logger("ImageDegrader", logger.logging.DEBUG)
        self.file_handler = file_handler.FileHandler()
        self.im = image_manipulator.ImageManipulator()
        self.time_take = time_take.TimeTake(debug=debug)
        self.debug = debug
    
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
            simple_noise=None,
            complex_noise=None,
            complex_noise_mode="gaussian",
            remove_black_borders=False,
            blur=None,
            simple_edge_detection=None,
            crop=None,
            rotate=None,
            resize=None,
            scale=None,
            quality=100,
            prefix="",
            suffix="",
        ):

        # check its path
        if not self.file_handler.verify_path(image_path):
            # make sure to not raise an error if its batch mode, because we want to continue
            if mode == "single":
                raise FileNotFoundError(f"Image at path \"{image_path}\" not found.")
            elif mode == "batch": 
                self.logger.error(f"Image at path \"{image_path}\" not found. Skipping image...")
            return

        self.logger.info(f"Processing image: \"{image_path}\"")

        # create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # open image
        image = self.im.open_image(image_path)
        
        # if image is invalid
        if image is None:
            if mode == "single":
                raise ValueError(f"Image at path \"{image_path}\" is invalid.")
            elif mode == "batch": 
                self.logger.error(f"Image at path \"{image_path}\" is invalid. Skipping image...")
                return

        if saturation:
            image = self.im.saturate(image, saturation)
        
        if brightness:
            image = self.im.brighten(image, brightness)
        
        if contrast:
            image = self.im.contrast(image, contrast)
        
        if sharpness:
            image = self.im.sharpen(image, sharpness)
        
        if simple_noise:
            image = self.im.simple_noise(image, noise)
        
        if complex_noise:
            image = self.im.complex_noise(image, noise, complex_noise_mode)

        if remove_black_borders:
            image = self.im.remove_black_borders(image)
        
        if blur:
            image = self.im.blur(image, blur)
        
        if simple_edge_detection:
            image = self.im.simple_edge_detection(image, simple_edge_detection)
        
        if crop:
            image = self.im.crop(image, crop)
        
        if rotate:
            image = self.im.rotate(image, rotate)
        
        if resize:
            image = self.im.resize(image, resize)
        
        if scale:
            image = self.im.scale(image, scale)
        
        # get image name without extension
        image_name = os.path.splitext(os.path.basename(image_path))[0]

        # output path with prefix and suffix and specified format/ext
        output_path = os.path.join(output_dir, f"{prefix}{image_name}{suffix}.{output_format}")

        self.im.save_image(image, output_path, quality=quality)
        
        self.logger.info(f"Image saved to \"{output_dir}\"")