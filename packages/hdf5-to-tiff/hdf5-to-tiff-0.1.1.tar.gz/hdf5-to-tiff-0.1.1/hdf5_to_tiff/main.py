'''
Copyright 1999 Illinois Institute of Technology

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL ILLINOIS INSTITUTE OF TECHNOLOGY BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Except as contained in this notice, the name of Illinois Institute
of Technology shall not be used in advertising or otherwise to promote
the sale, use or other dealings in this Software without prior written
authorization from Illinois Institute of Technology.
'''

import sys
import argparse
from hdf5_to_tiff import __version__
from hdf5_to_tiff.modules.exception_handler import handlers
from hdf5_to_tiff.modules.viewerGUI import viewerGUI, generate_tiff_files_headless
from hdf5_to_tiff.modules.pyqt_utils import *

if sys.platform in handlers:
    sys.excepthook = handlers[sys.platform]

def main():
    parser = argparse.ArgumentParser(
    description='The script will generate the tiff files from the given hdf5 file. Metadata will be read from the given metadata file and added as an ImageDescription tag in all the tiff files.')
    parser.add_argument('-h5', metavar='hdf5', help='Path to the Hdf5 file', nargs='*')
    parser.add_argument('-m', metavar='metadata', help='Path to the metadata text file')
    parser.add_argument('-z', action='store_true', help='Generate a compressed version of the TIF images')

    args = parser.parse_args()
    compress = args.z
    h5_filename = args.h5
    if not h5_filename:
        print(parser.format_help())
        print("\nHDF5 to TIFF Converter v"+str(__version__))
        app = QApplication(sys.argv)
        myapp = viewerGUI()
        sys.exit(app.exec_())
    else:
        #files = glob.glob(h5_filename)
        for f in h5_filename:
            print(f)
            path = os.path.dirname(os.path.abspath(f))
            prefix = os.path.basename(f).rsplit('.', 1)[0]
            # metadata = ''
            # if args.m:
            #     metadata = read_meta_data(args.m)
            
            generate_tiff_files_headless(f, path, prefix, compress)

if __name__ == "__main__":
    main()
