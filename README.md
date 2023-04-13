# ImageToMap
Script designed to convert an image to a `.xml` file representing a valid map input
for the Mosquito game provided in Spring 2023's iteration of CIS 5590 at the
University of Pennsylvania.

## Installation
### Conda installation:

1. Clone repo:
```
~$ git clone git@github.com:wyomatthew/ImageToMap.git
~$ cd ImageToMap
~/ImageToMap$ 
```
2. Install dependencies
```
~/ImageToMap$ conda env create -f env.yml
~/ImageToMap$ conda activate ComputerVision
~/ImageToMap$ 
```
3. Test installation
```
~/ImageToMap$ python3 Main.py --help
Usage: Main.py [OPTIONS] FILE_PATH

Options:
  --make-img                  if True, outputs the created lines to an image file
  --length-threshold INTEGER  segments shorter than this will be discarded
  --distance-threshold FLOAT  a point placed from a hypothesis line segment farther than this will be regarded as an outlier
  --canny-th1 FLOAT           lower threshold in canny alg: https://docs.opencv.org/4.x/da/d22/tutorial_py_canny.html
  --canny-th2 FLOAT           upper threshold in canny alg: https://docs.opencv.org/4.x/da/d22/tutorial_py_canny.html
  --aperture-size INTEGER     size of kernel in canny alg
  --help                      Show this message and exit.
~/ImageToMap$ 
```
### Pip installation
TODO
For now, you can manually install the requirements laid out in `env.yml`.

## Usage
All usage information can be retrieved by running the script `Main.py` with
the `--help` argument. An example follows:
```
~/ImageToMap$ python3 Main.py java.jpg
~/ImageToMap$ 
```
This will create the file `java.xml` in the working directory which can be used
as an input map.
