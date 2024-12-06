import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def init():
    plot_image.set_data(np.zeros((height, width)))
    plot_image.set_alpha(0)
    return plot_image,

def add_galaxy_to_mosaic(frame, all_images):

    image_index = frame // 3
    image_array = all_images[image_index]

    # Performing a logarithmic transformation of the image data
    #scaling_constant = 255/np.log(1 + np.max(image_array))

    # For fading in
    # Gradually increase alpha from 0 to 1 after initial frame
    if frame == 0:
        alpha = 1

    elif frame % 3 == 0:
        alpha = 0

    #elif frame % 3 == 1:
    #    alpha = 0.5

    elif (frame % 3) != 0:
        alpha = min((frame / 3), 1)

    else:
        alpha = 1

    #plot_image.set_alpha(alpha)

    # Display the FITS image after scaling
    plot_image = ax.imshow(image_array, cmap = 'gray', alpha = alpha)
    # _ = ax.imshow(scaling_constant * np.log(1 + image_array), cmap='gray')

    # Show the plot
    # plt.show()

    # Save the plot
    #_ = fig.savefig(filename, dpi = fig.dpi, bbox_inches = 'tight')

    return plot_image,

def generate_animation(
        all_images,
        time_step,
        filename = "animation.gif"
):
    # Clear any existing plots
    plt.clf()
    # Create a figure
    #global ax, plot_image, height, width
    fig, ax = plt.subplots()

    ax.set_title('Galaxy Mosaic')
    # ax.set_xlabel('X-axis')
    # ax.set_ylabel('Y-axis')
    ax.invert_yaxis()
    # Create an animation

    #height, width = np.shape(all_images[0])
    #plot_image = ax.imshow(np.zeros((height, width)), cmap = "gray", alpha = 1)

    # ims is a list of lists, each row is a list of artists to draw in the
    # current frame; here we are just animating one artist, the image, in
    # each frame
    ims = []
    previous_images = []

    # show an initial image first
    ax.imshow(all_images[0], alpha = 1, cmap = "gray")

    num_images = len(all_images)
    dim = num_images * 2
    initial_alphas = np.zeros((dim, dim))
    lower_triangular = np.tril_indices(dim)
    # lower_triangular_add_on = np.tril_indices(cols - 1)
    lowest_row = [1 - (i / dim) for i in range(dim)]
    add_on = np.tile(lowest_row, (dim, 1))
    for pos in zip(*lower_triangular):
        x = pos[0]
        y = pos[1]
        alpha = (x - y) / (dim - 1)
        initial_alphas[pos] = min(alpha, 1)

        add_on[x, :] += 1 / (dim - 1)

    #last_add_on = np.ones(((dim - 1), dim))
    initial_alphas = np.vstack((initial_alphas, add_on)) #, last_add_on))
    initial_alphas[initial_alphas > 1] = 1

    all_images_for_animation = np.array([all_images] * len(all_images))
    ims = [
        [
            ax.imshow(
                    all_images_for_animation[r, c],
                    animated = True,
                    alpha = alpha,
                    cmap = "gray"
            )
        ]
        for r, row in enumerate(initial_alphas)
        for c, alpha in enumerate(row)
    ]

    ani = animation.ArtistAnimation(
            fig,
            ims,
            #add_galaxy_to_mosaic,
            interval = time_step * 100, # milliseconds
            blit = True
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