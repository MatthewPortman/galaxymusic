import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def init():
    plot_image.set_data(np.zeros((height, width)))
    plot_image.set_alpha(0)
    return plot_image,

# def calculate_alpha(dim):
#     # As a triangular matrix
#     alphas = np.zeros((dim, dim))
#     lower_triangular = np.tril_indices(dim)
#     # lower_triangular_add_on = np.tril_indices(cols - 1)
#     lowest_row = [1 - (i / dim) for i in range(dim)]
#     add_on = np.tile(lowest_row, (dim, 1))
#     for pos in zip(*lower_triangular):
#         x = pos[0]
#         y = pos[1]
#         alpha = (x - y) / (dim - 1)
#         alphas[pos] = min(alpha, 1)
#
#         add_on[x, :] += 1 / (dim - 1)
#
#     last_add_on = np.ones((dim , dim))
#     alphas = np.vstack((alphas, add_on, last_add_on))
#     alphas[alphas > 1] = 1
#
#     return alphas

def add_galaxy_to_mosaic(
        frame              : int,
        all_images         : list[np.ndarray],
        lengthening_factor : int,
        save            = False,
        filename        = "mosaic.jpg",
        save_alpha      = np.ones((1000,1000)),
        secondary_image = None
) -> tuple[plt.imshow]:
    # Clear any existing plots
    plt.clf()

    image_index = frame // lengthening_factor
    image_array = all_images[image_index]

    alpha = min((frame % lengthening_factor) / (lengthening_factor / 2), 1)
    if frame <= lengthening_factor:
        alpha = 1

    if save:
        # Thanks to this answer for the help (issue saving square image)
        # https://stackoverflow.com/a/34769840
        dpi = 100
        height, width = np.shape(image_array)

        # Size of the figure to fit the image
        figsize = width / float(dpi), height / float(dpi)

        # Create a figure of the right size with one axes that takes up the full figure
        fig = plt.figure(figsize = figsize)
        ax  = fig.add_axes([0, 0, 1, 1])

    # Display the FITS image after scaling
    plot_image = ax.imshow(image_array, cmap='gray', alpha = alpha)

    # Show the plot
    # plt.show()

    if save:
        # Display the secondary image (overplotted faded new galaxy) image
        new_plot_image = ax.imshow(secondary_image, cmap = 'gray', alpha = save_alpha)

        ax.axis('off')

        plt.gcf().set_size_inches(5, 5)
        # Save the plot
        _ = fig.savefig(
                filename,
                dpi = dpi,
                bbox_inches = 'tight',
                pad_inches = 0.0
        )
        plt.close(fig)

    return plot_image,

def generate_animation(
        all_images,
        time_step,
        filename = "animation.gif"
):
    # Clear any existing plots
    plt.clf()
    # Create a figure
    global ax, fig, plot_image, height, width
    fig, ax = plt.subplots()

    ax.set_title('Galaxy Mosaic')
    # ax.set_xlabel('X-axis')
    # ax.set_ylabel('Y-axis')
    ax.invert_yaxis()
    # Create an animation

    height, width = np.shape(all_images[0])
    plot_image = ax.imshow(np.zeros((height, width)), cmap = "gray", alpha = 1)

    lengthening_factor = 3

    # alphas = calculate_alpha(len(all_images))

    ani = animation.FuncAnimation(
            fig,
            add_galaxy_to_mosaic,
            init_func = init,
            frames    = len(all_images) * lengthening_factor,
            fargs     = (all_images, lengthening_factor,),
            interval  = time_step * 1000, # milliseconds
            blit      = True
    )

    ani.save(filename, writer = 'imagemagick')

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