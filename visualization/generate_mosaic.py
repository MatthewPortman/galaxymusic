import numpy as np
import matplotlib.pyplot as plt

def generate_mosaic(image_array, fig = None, ax = None, filename = "mosaic.png"):
    if fig is None or ax is None:
        # Clear any existing plots
        plt.clf()

        # Create a figure and subplots
        fig, ax = plt.subplots(1, 1, figsize = (10, 10))

    # Performing a logarithmic transformation of the image data
    scaling_constant = 255/np.log(1 + np.max(image_array))

    # Display the FITS image after scaling
    # image_fits = ax.imshow(scaling_constant * np.log(1 + image_data_fits), cmap='gray')
    _ = ax.imshow(scaling_constant * np.log(1 + image_array), cmap='gray')

    ax.set_title('Galaxy Mosaic')
    # ax.set_xlabel('X-axis')
    # ax.set_ylabel('Y-axis')
    ax.invert_yaxis()

    # Show the plot
    # plt.show()

    # Save the plot
    _ = fig.savefig(filename, dpi = fig.dpi, bbox_inches = 'tight')

    return fig, ax

# from PIL import Image
#
# width = 1000
# height = 1000
# mosaic_size = (width, height)
#
# # TODO: Create as animation, with each frame being a different galaxy
# # can do this by adding each FITS to a numpy array
# canvas = Image.new('L', mosaic_size, color = 'black')
#
# transparency_cutoff = 15
# for model_galaxy in all_models:
#     x_pos = randint(0, width  - 150)
#     y_pos = randint(0, height - 150)
#
#     image_galaxy = Image.fromarray(model_galaxy).convert("LA")
#     alpha_array  = np.zeros_like(model_galaxy)
#     #alpha_array[model_galaxy < np.log(15)]  = 0
#     alpha_array[model_galaxy >= np.log(100)]  = 255
#
#     for i, alpha_value in enumerate(range(transparency_cutoff, 200, 5)):
#         conditions = (
#                 (model_galaxy >= np.log((i + 1)*transparency_cutoff)) &
#                 (model_galaxy < np.log((i + 2) * transparency_cutoff))
#         )
#         alpha_array[conditions] = alpha_value
#
#     alpha_image = Image.fromarray(alpha_array).convert("L")
#
#     canvas.paste(image_galaxy, (x_pos, y_pos), alpha_image)
#
# #canvas.save("mosaic.png")
# canvas