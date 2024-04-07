import os
import shutil



class FileHandler:
    def __init__(self):
        pass
    
    @staticmethod
    def verify_path(path):
        """
        Verify if the path exists.
        :param path: str: The path to verify
        :return: bool: True if the path exists, False otherwise
        """
        if not os.path.exists(path):
            return False
        return True

    # get all images in a directory
    def get_images(self, dir_path):
        """
        Get all images in a directory.
        :param path: str: The path to the directory
        :return: list: A list of all images in the directory
        """
        # verify path first
        if not self.verify_path(dir_path):
            raise FileNotFoundError(f"Folder path \"{dir_path}\" not found.")
        
        images = []
        for file in os.listdir(dir_path):
            if file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".png"):
                images.append(os.path.join(dir_path, file))

        return images
    
    def create_directory(self, path):
        """
        Create a directory.
        :param path: str: The path to the directory
        """
        if not self.verify_path(path):
            os.makedirs(path)
    
    def remove_directory(self, path):
        """
        Remove a directory.
        :param path: str: The path to the directory
        """
        if self.verify_path(path):
            shutil.rmtree(path)
    
    def remove_file(self, path):
        """
        Remove a file.
        :param path: str: The path to the file
        """
        if self.verify_path(path):
            os.remove(path)
