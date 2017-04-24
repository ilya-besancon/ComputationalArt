""" @ilya-besancon
This is the updated version of the computational art program.
I modified my code to implement lambda values.
"""

import random
import math
from PIL import Image

# lambda functions:
l_x = lambda x, y, z: x
l_y = lambda x, y, z: y
l_t = lambda x, y, z: z
l_cos_pi = lambda x, y, z: math.cos(math.pi * x)
l_sin_pi = lambda x, y, z: math.sin(math.pi * x)
l_avg = lambda x, y, z: (x + y + z)/3
l_prod = lambda x, y, z: (x*y*z)
l_power = lambda x, y, z: x**2
l_add_third = lambda x, y, z: (x+y+z)/3
list_functions = [l_x, l_y, l_t, l_cos_pi, l_sin_pi,
                  l_avg, l_prod, l_power, l_add_third]


def build_random_function(depth):
    """ Builds a random function of a given depth
        returns: nested list of lambda functions,
         which take (x,y,z) input in generate_art()
    """
    # depth = random.randint(0, max_depth - min_depth)
    # min_depth = min_depth + depth
    # max_depth = min_depth
    if depth <= 1:
        new_int = random.randint(0, 2)
        return list_functions[new_int]

    else:
        picker = random.randint(3, 8)
        f1 = build_random_function(depth - 1)
        f2 = build_random_function(depth - 1)
        f3 = build_random_function(depth - 3)
        return lambda x, y, t: list_functions[picker](f1(x, y, t),
                                                      f2(x, y, t), f3(x, y, t))


def remap_interval(val,
                   input_interval_start,
                   input_interval_end,
                   output_interval_start,
                   output_interval_end):
    input_range = input_interval_end - input_interval_start
    output_range = output_interval_end - output_interval_start
    ratio = output_range/input_range
    # print(val)
    # print(input_interval_start)
    newval = (val - input_interval_start) * ratio + output_interval_start
    return newval

# remap_interval(5,4,6,0,2)

    """ Given an input value in the interval [input_interval_start,
        input_interval_end], return an output value scaled to fall within
        the output interval [output_interval_start, output_interval_end].

        val: the value to remap
        input_interval_start: the start of the interval that contains all
                              possible values for val
        input_interval_end: the end of the interval that contains all possible
                            values for val
        output_interval_start: the start of the interval that contains all
                               possible output values
        output_inteval_end: the end of the interval that contains all possible
                            output values
        returns: the value remapped from the input to the output interval

        >>> remap_interval(0.5, 0, 1, 0, 10)
        5.0
        >>> remap_interval(5, 4, 6, 0, 2)
        1.0
        >>> remap_interval(5, 4, 6, 1, 2)
        1.5
    """


def color_map(val):
    """ Maps input value between -1 and 1 to an integer 0-255, suitable for
        use as an RGB color code.

        val: value to remap, must be a float in the interval [-1, 1]
        returns: integer in the interval [0,255]

        >>> color_map(-1.0)
        0
        >>> color_map(1.0)
        255
        >>> color_map(0.0)
        127
        >>> color_map(0.5)
        191
    """
    # NOTE: This relies on remap_interval, which you must provide
    color_code = remap_interval(val, -1, 1, 0, 255)
    return int(color_code)


def test_image(filename, x_size=350, y_size=350):
    """ Generate test image with random pixels and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (random.randint(0, 255),  # Red channel
                            random.randint(0, 255),  # Green channel
                            random.randint(0, 255))  # Blue channel

    im.save(filename)


def generate_art(filename, x_size=350, y_size=350, z=70):
    """ Generate computational art and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for red, green, and blue channels - where the magic happens!
    depth = 5
    red_function = build_random_function(depth)
    green_function = build_random_function(depth)
    blue_function = build_random_function(depth)

    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (
                    # functions are directly evaluated, instead of using evaluate_random_function()
                    color_map(red_function(x, y, z)),
                    color_map(green_function(x, y, z)),
                    color_map(blue_function(x, y, z))
                    # color_map(evaluate_random_function(red_function, x, y)),
                    # color_map(evaluate_random_function(green_function, x, y))
                    # color_map(evaluate_random_function(blue_function, x, y))
                    )

    im.save(filename)


if __name__ == '__main__':
    # import doctest
    # doctest.testmod()

    # Create some computational art!
    # TODO: Un-comment the generate_art function call after you
    #       implement remap_interval and evaluate_random_function
    generate_art("myart_l_3.png")

    # Test that PIL is installed correctly
    # TODO: Comment or remove this function call after testing PIL install
    # test_image("noise.png")
