import math
import sys
from pathlib import Path

from matplotlib import pyplot
from matplotlib.patches import Rectangle

# import our basic, light-weight png reader library
import imageIO.png

# this function reads an RGB color png file and returns width, height, as well as pixel arrays for r,g,b
def readRGBImageToSeparatePixelArrays(input_filename):

    image_reader = imageIO.png.Reader(filename=input_filename)
    # png reader gives us width and height, as well as RGB data in image_rows (a list of rows of RGB triplets)
    (image_width, image_height, rgb_image_rows, rgb_image_info) = image_reader.read()

    print("read image width={}, height={}".format(image_width, image_height))

    # our pixel arrays are lists of lists, where each inner list stores one row of greyscale pixels
    pixel_array_r = []
    pixel_array_g = []
    pixel_array_b = []

    for row in rgb_image_rows:
        pixel_row_r = []
        pixel_row_g = []
        pixel_row_b = []
        r = 0
        g = 0
        b = 0
        for elem in range(len(row)):
            # RGB triplets are stored consecutively in image_rows
            if elem % 3 == 0:
                r = row[elem]
            elif elem % 3 == 1:
                g = row[elem]
            else:
                b = row[elem]
                pixel_row_r.append(r)
                pixel_row_g.append(g)
                pixel_row_b.append(b)

        pixel_array_r.append(pixel_row_r)
        pixel_array_g.append(pixel_row_g)
        pixel_array_b.append(pixel_row_b)

    return (image_width, image_height, pixel_array_r, pixel_array_g, pixel_array_b)


# a useful shortcut method to create a list of lists based array representation for an image, initialized with a value
def createInitializedGreyscalePixelArray(image_width, image_height, initValue = 0):

    new_array = [[initValue for x in range(image_width)] for y in range(image_height)]
    return new_array


def computeRGBToGreyscale(pixel_array_r, pixel_array_g, pixel_array_b, image_width, image_height):
    
    greyscale_pixel_array = createInitializedGreyscalePixelArray(image_width, image_height)
    
    for i in range(image_height):
        for j in range(image_width):
            greyscale_pixel_array[i][j] = round(0.299*pixel_array_r[i][j] + 0.587*pixel_array_g[i][j] + 0.114*pixel_array_b[i][j])
    
    return greyscale_pixel_array

def scaleTo0And255AndQuantize(pixel_array, image_width, image_height):
    array_greyscale = createInitializedGreyscalePixelArray(image_width, image_height)
    min = 256
    max = -1
    for i in range(image_height):
        for j in range(image_width):
            if (pixel_array[i][j] < min):
                min = pixel_array[i][j]
            if (pixel_array[i][j] > max):
                max = pixel_array[i][j]
        
    range_vals = max-min
    if range_vals == 0:
        multiplier = 0
    else:
        multiplier = 255/range_vals
        
    for i in range(image_height):
        for j in range(image_width):
            array_greyscale[i][j] = round((pixel_array[i][j]-min)*multiplier)
            if array_greyscale[i][j] == -1:
                array_greyscale[i][j] = 0
            
    return array_greyscale

def computeStandardDeviationImage5x5(pixel_array, image_width, image_height):
    
    end_result = createInitializedGreyscalePixelArray(image_width, image_height, 0.0)
    
    for i in range(2, image_height-2):
        for j in range(2, image_width-2):
            pixel_sum = 0
            for x in range(-2, 3):
                for y in range(-2, 3):
                    pixel_sum = pixel_sum + pixel_array[i+x][j+y]

            mean = (1/25) * pixel_sum

            variance_sum = 0
            for x in range(-2, 3):
                for y in range(-2, 3):
                    variance_sum = variance_sum + (pixel_array[i+x][j+y] - mean)**2

            deviation = (variance_sum/25)**0.5
            
            end_result[i][j] = deviation
    
    return end_result

def computeThresholdGE(pixel_array, threshold_value, image_width, image_height):
    for i in range(image_height):
        for j in range(image_width):
            if (pixel_array[i][j] >= threshold_value):
                pixel_array[i][j] = 255
            else:
                pixel_array[i][j] = 0
    return pixel_array

def computeDilation8Nbh3x3FlatSE(pixel_array, image_width, image_height):
    
    end_array = createInitializedGreyscalePixelArray(image_width, image_height)
    
    new_array = createInitializedGreyscalePixelArray(image_width+2, image_height+2)
    
    for j in range(0, image_width):
        for i in range(0, image_height):
            new_array[i+1][j+1] = pixel_array[i][j]
    
    for i in range(1, image_height+1):
        for j in range(1, image_width+1):
            
            sumn = 0
            
            for x in range(3):
                for y in range(3):
                    if new_array[x+i-1][y+j-1] > 0:
                        sumn = sumn + 1
            
            if sumn > 0:
                end_array[i-1][j-1] = 1
                
    return end_array

# This is our code skeleton that performs the license plate detection.
# Feel free to try it on your own images of cars, but keep in mind that with our algorithm developed in this lecture,
# we won't detect arbitrary or difficult to detect license plates!
def main():

    command_line_arguments = sys.argv[1:]

    SHOW_DEBUG_FIGURES = True

    # this is the default input image filename
    input_filename = "numberplate1.png"

    if command_line_arguments != []:
        input_filename = command_line_arguments[0]
        SHOW_DEBUG_FIGURES = False

    output_path = Path("output_images")
    if not output_path.exists():
        # create output directory
        output_path.mkdir(parents=True, exist_ok=True)

    output_filename = output_path / Path(input_filename.replace(".png", "_output.png"))
    if len(command_line_arguments) == 2:
        output_filename = Path(command_line_arguments[1])


    # we read in the png file, and receive three pixel arrays for red, green and blue components, respectively
    # each pixel array contains 8 bit integer values between 0 and 255 encoding the color values
    (image_width, image_height, px_array_r, px_array_g, px_array_b) = readRGBImageToSeparatePixelArrays(input_filename)

    # setup the plots for intermediate results in a figure
    fig1, axs1 = pyplot.subplots(2, 2)
    axs1[0, 0].set_title('Input red channel of image')
    axs1[0, 0].imshow(px_array_r, cmap='gray')
    axs1[0, 1].set_title('Input green channel of image')
    axs1[0, 1].imshow(px_array_g, cmap='gray')
    axs1[1, 0].set_title('Input blue channel of image')
    axs1[1, 0].imshow(px_array_b, cmap='gray')


    # STUDENT IMPLEMENTATION here

    # Removing RGB for greyscale
    px_array = computeRGBToGreyscale(px_array_r, px_array_g, px_array_b, image_width, image_height)

    # Scaling to take up full 8 bit scale
    px_array = scaleTo0And255AndQuantize(px_array, image_width, image_height)

    # Taking standard deviation in a 5x5 range around each pixel (shows more clearly where groupings are, like a license plate)
    px_array = computeStandardDeviationImage5x5(px_array, image_width, image_height)

    # Scaling to take up full 8 bit scale
    px_array = scaleTo0And255AndQuantize(px_array, image_width, image_height)

    # Making light pixels white and dark pixels black
    px_array = computeThresholdGE(px_array, 150, image_width, image_height)

    # Connecting places that are heavy in white/black
    for i in range(3):
        px_array = computeDilation8Nbh3x3FlatSE(px_array, image_width, image_height)


        

    # compute a dummy bounding box centered in the middle of the input image, and with as size of half of width and height
    center_x = image_width / 2.0
    center_y = image_height / 2.0
    bbox_min_x = center_x - image_width / 4.0
    bbox_max_x = center_x + image_width / 4.0
    bbox_min_y = center_y - image_height / 4.0
    bbox_max_y = center_y + image_height / 4.0





    # Draw a bounding box as a rectangle into the input image
    axs1[1, 1].set_title('Final image of detection')
    axs1[1, 1].imshow(px_array, cmap='gray')
    rect = Rectangle((bbox_min_x, bbox_min_y), bbox_max_x - bbox_min_x, bbox_max_y - bbox_min_y, linewidth=1,
                     edgecolor='g', facecolor='none')
    axs1[1, 1].add_patch(rect)



    # write the output image into output_filename, using the matplotlib savefig method
    extent = axs1[1, 1].get_window_extent().transformed(fig1.dpi_scale_trans.inverted())
    pyplot.savefig(output_filename, bbox_inches=extent, dpi=600)

    if SHOW_DEBUG_FIGURES:
        # plot the current figure
        pyplot.show()


if __name__ == "__main__":
    main()