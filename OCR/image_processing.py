import cv2
import os


# pdf_image_path = os.listdir("PDF_IMAGE")


# print(pdf_image_path)
# class Image_processing:
#     def __init__(self):
#         self.processing()
    
#     def processing(self):
#         for i, image in enumerate(pdf_image_path):
#             process_image = cv2.imread(image)
#             gray = cv2.cvtColor(process_image, cv2.COLOR_BGR2GRAY)
#             _, black_white = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
#             result = cv2.bitwise_not(black_white)
#             os.makedirs("PROCESS_PDF_IMAGE", exist_ok = True)
#             final_path = os.path.join("PROCESS_PDF_IMAGE", f"page_{process_image[:-4]}_{i+1}_processed.png")
#             cv2.imwrite(final_path, result)
#             os.remove(pdf_image_path)

# if __name__ == "__main__":
#     Image_processing()