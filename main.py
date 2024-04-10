from image_degrader import degrader



def single_process(image_path):
    image_degrader = degrader.ImageDegrader()

    image_degrader.degrade_image(
        image_path=image_path,
        simple_edge_detection=10,
    )

def batch_process(image_dir):
    image_degrader = degrader.ImageDegrader()

    # get all images in the directory
    images_list = image_degrader.file_handler.get_images(image_dir)

    # loop through all images and manipulate them
    for image_path in images_list:
        image_degrader.degrade_image(
            image_path=image_path,
            simple_edge_detection=10,
            output_format="png",
        )

if __name__ == "__main__":
    # ====  example: single image  ====
    image_path = str(input("Image path: "))
    single_process(image_path)

    # ====  example: batch process  ====
    # images_dir = str(input("Images dir path: "))
    # batch_process(images_dir)
