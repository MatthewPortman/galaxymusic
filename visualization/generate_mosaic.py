import numpy as np
import matplotlib.pyplot as plt

def generate_mosaic(image_array, filename = "mosaic.png"):
    plt.clf()
    # Create a figure and subplots
    fig, ax1 = plt.subplots(1, 1, figsize=(10, 10))

    # Performing a logarithmic transformation of the image data
    scaling_constant = 255/np.log(1 + np.max(image_array))

    # Display the FITS image after scaling
    # image_fits = ax1.imshow(scaling_constant * np.log(1 + image_data_fits), cmap='gray')
    _ = ax1.imshow(scaling_constant * np.log(1 + image_array), cmap='gray')

    # Create a slider widget for the FITS image
    # slider_fits = widgets.FloatSlider(value = 1.0, min = 0.0, max = 2.0, step=0.01, description='FITS Scale:', continuous_update=True)

    # Function to update the FITS image when slider value changes
    # def update_image_fits(change):
    #     # Update the image data based on the slider value
    #     new_image_data_fits = change.new * np.log(1 + image_data_fits)
    #
    #     # Update the FITS image with new data
    #     image_fits.set_data(new_image_data_fits)
    #
    #     # Redraw the figure
    #     fig.canvas.draw()

    # Attach the update_image_fits function to the FITS slider's value change event
    # slider_fits.observe(update_image_fits, 'value')

    # Display the slider widgets
    # display(widgets.HBox([slider_fits])) #, slider_array]))

    # Add any additional customization you need to the subplots
    ax1.set_title('FITS Image')
    ax1.set_xlabel('X-axis')
    ax1.set_ylabel('Y-axis')
    ax1.invert_yaxis()

    # Show the plot
    # plt.show()
    fig.savefig(filename, dpi = fig.dpi)

    return fig

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