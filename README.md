# Image_Compression_with_SPARK
In this project, I use the MapReduce programming paradigm to parallelize a common image compression algorithm in Spark to process multiple images at once.

## Background
There have always been different methods of video compression in order to adapt videos to be rendered more easily on devices with less memory or computing capacity. We will be implementing a scheme using the Discrete Cosine Transform (DCT) to perform video compression. This form of lossy compression encoding is typicaly used alongside lossless compression to compress video files. For the purposes of this project, we will only focus on the lossy aspect.

## Running
Run :
```spark-submit run_image_processor.py -i INPUT_FILE -o OUTPUT_FILE```

Then you can run:

```image_diff.py -f1 OUTPUT_FILE -f2 REF_OUTPUT_FILE```