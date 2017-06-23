import pyspark
from pyspark import SparkContext
import cv2
import numpy as np 
import scipy as sp
import struct
from helper_functions import *
from constants import *


### WRITE ALL HELPER FUNCTIONS ABOVE THIS LINE ###

def generate_Y_cb_cr_matrices(rdd):
    """
    THIS FUNCTION MUST RETURN AN RDD
    """
    ### BEGIN SOLUTION ###

    def convert(pair):
        key = pair[0]
        img = pair[1]
        img = convert_to_YCrCb(img)

        height = img.shape[0]
        weight = img.shape[1]
        y_tuple = ((key, height, width), ("y", img[0]))
        cb_tuple = ((key, height, width), ("cb", img[1]))
        cr_tuple = ((key,height, width), ("cr", img[2]))
        return (y_tuple, cb_tuple, cr_tuple)

    rdd = rdd.flatMap(convert)
    return rdd

def generate_sub_blocks(rdd):
    """
    THIS FUNCTION MUST RETURN AN RDD
    """
    ### BEGIN SOLiUTION ###


    def break8(pair):
        key = pair[0]
        level = pair[1][0]
        img = pair[1][1]
        
        all_eights = []     
        height = key[1]
        width = key[2]
        for row in range(0, height, 8):
            for col in range(0, width, 8):
                img_eights = np.zeros((8, 8), np.uint8)
                for i in range(8):
                    for j in range(8):
                        img_eights[i][j] = img[row+i][col+j]
                new_eight = (key, (level, row, col, img_eights))
                all_eights.append(new_eight)

        return all_eights
    
    rdd = rdd.flatMap(break8)
    return rdd

def apply_transformations(rdd):
    """
    THIS FUNCTION MUST RETURN AN RDD
    """
    ### BEGIN SOLUTION ###

    def transform(pair):
        key = pair[0]
        level = pair[1][0]
        eight = pair[1][3]
        eight = np.array([x - 128 for x in eight])
            # DCT
        eight = dct_block(eight)
            # Quant
        is_y = (level == "y")
        eight = quantize_block(eight, is_y)
            # Inverse Quant
        eight = quantize_block(eight, is_y, inverse=True)
            # Inverse DCT
        eight = dct_block(eight, True)
            # Add back the 128 we subtracted before
        eight = np.array([x + 128 for x in eight])

        pair[1][3] = eight
        new_eight = (key, pair[1])
        return new_eight

    rdd = rdd.map(transform)    
    return rdd


def combine_sub_blocks(rdd):
    """
    Given an rdd of subblocks from many different images, combine them together to reform the images.
    Your rdd should contain values that are np arrays of size (height, width).

    THIS FUNCTION MUST RETURN AN RDD
    """
    ### BEGIN SOLUTION ###

    def combine(block1, block2):
        list1 = block1
        list2 = block2
        return [list1] + [list2]

    def map(pair):
        height = pair[0][1]
        width = pair[0][2]
        all_sublocks = pair[1]
        Y_matrix = np.zeros((height, width), np.uint8)
        Cb_matrix = np.zeros((height, width), np.uint8)
        Cr_matrix = np.zeros((height, width), np.uint8)
        for sublock in all_sublocks:
            level = sublock[0]
            if level = "y":
                populate(Y_matrix, sublock[1], sublock[2], sublock[3])
            elif level = "cb":
                populate(Cb_matrix, sublock[1], sublock[2], sublock[3])
            elif level = "cr":
                populate(Cr_matrix, sublock[1], sublock[2], sublock[3])
        
        #final_image = np.zeros((height, width, 3), np.uint8)
        return (key, np.array([Y_matrix, Cb_matrix, Cr_matrix]))

    rdd = rdd.reducebykey(combine)
    rdd = rdd.map(map)
    return rdd


def run(images):
    """
    THIS FUNCTION MUST RETURN AN RDD

    Returns an RDD where all the images will be proccessed once the RDD is aggregated.
    The format returned in the RDD should be (image_id, image_matrix) where image_matrix 
    is an np array of size (height, width, 3).
    """
    test_ycbcr()
    a = 1 / 0


    sc = SparkContext()
    rdd = sc.parallelize(images, 16) \
        .map(truncate).repartition(16)
    rdd = generate_Y_cb_cr_matrices(rdd)
    rdd = generate_sub_blocks(rdd)
    rdd = apply_transformations(rdd)
    rdd = combine_sub_blocks(rdd)

    ### BEGIN SOLUTION HERE ###
    # Add any other necessary functions you would like to perform on the rdd here
    # Feel free to write as many helper functions as necessary
    return  rdd


def populate(matrix, row, col, sublock):
    for i in range(8):
        for j in range(8):
            new_row = row * 8 + i
            new_col = col * 8 + j
            matrix[new_col][new_row] = sublock[i][j]



        

def test_ycbcr():


    arr = np.zeros((8, 8))
    for i in range(8):
        for j in range(8):
            arr[i][j] = (i*8) + j
    arr2 = arr[:]
    arr3 = arr[:]
    arr4 = (arr, arr2, arr3)

    pair = (1, arr4)
    q = generate_sub_blocks(pair)
    print(q)
    




