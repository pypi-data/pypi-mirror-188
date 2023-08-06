"""
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
"""

import os
import glob
import fabio
import numpy as np
from PIL import Image
from os.path import join, split
from hdf5_to_tiff import __version__
from hdf5_to_tiff.modules.pyqt_utils import *

class viewerGUI(QMainWindow):
    """
    A class for GUI of Image Merger
    """
    def __init__(self):
        """
        Initial window
        """
        QWidget.__init__(self)
        self.img_list = []
        self.img_grps = []
        self.stop_process = False
        self.initUI()
        self.setConnections()

    def initUI(self):
        """
        initial all widgets
        """
        self.setWindowTitle("HDF5 to TIFF Converter v." + __version__)
        self.centralWid = QWidget(self)
        self.setCentralWidget(self.centralWid)
        self.mainLayout = QGridLayout(self.centralWid)

        self.in_directory = QLineEdit()
        self.select_in_folder = QPushButton("Browse")
        self.out_directory = QLineEdit()
        self.select_out_folder = QPushButton("Browse")

        self.detailGrp = QGroupBox("Logs")
        self.detailLayout = QVBoxLayout(self.detailGrp)
        self.detail = QPlainTextEdit()
        self.detail.setReadOnly(True)
        self.progressbar = QProgressBar()
        self.detailLayout.addWidget(self.detail)
        self.detailLayout.addWidget(self.progressbar)

        self.start_button = QPushButton("Start")
        self.start_button.setCheckable(True)

        self.compressChkBx = QCheckBox("Compress the Resulting Images")
        self.compressChkBx.setChecked(False)

        self.mainLayout.addWidget(QLabel("Input Directory : "), 0, 0, 1, 1)
        self.mainLayout.addWidget(self.in_directory, 0, 1, 1, 1)
        self.mainLayout.addWidget(self.select_in_folder, 0, 2, 1, 1)

        self.mainLayout.addWidget(QLabel("Output Directory : "), 1, 0, 1, 1)
        self.mainLayout.addWidget(self.out_directory, 1, 1, 1, 1)
        self.mainLayout.addWidget(self.select_out_folder, 1, 2, 1, 1)

        self.mainLayout.addWidget(self.detailGrp, 4, 0, 1, 3)
        self.mainLayout.addWidget(self.start_button, 5, 0, 1, 3, Qt.AlignCenter)

        self.mainLayout.addWidget(self.compressChkBx, 3, 0, 1, 3)

        self.mainLayout.columnStretch(1)
        self.mainLayout.rowStretch(3)
        self.resize(800, 400)
        self.show()

    def setConnections(self):
        """
        Set handler for all widgets
        """
        self.select_in_folder.clicked.connect(self.browse_input)
        self.select_out_folder.clicked.connect(self.browse_output)
        self.start_button.toggled.connect(self.start_clicked)

    def browse_input(self):
        """
        Handle when Browse for input folder is clicked
        :return:
        """
        path = getAFile()
        if len(path) > 0:
            self.in_directory.setText(path)
            dir_path, _ = split(str(path))
            self.out_directory.setText(join(dir_path, 'converted_tiffs'))
            QApplication.processEvents()

    def browse_output(self):
        """
        Handle when Browse for output folder is clicked
        :return:
        """
        path = getAFolder()
        if len(path) > 0:
            self.out_directory.setText(path)

    def start_clicked(self):
        """
        handle when Start is clicked
        :return:
        """
        if self.start_button.text() == 'Start':
            self.stop_process = False
            self.start_button.setText("Stop")
            self.in_directory.setEnabled(False)
            self.select_in_folder.setEnabled(False)
            self.out_directory.setEnabled(False)
            self.select_out_folder.setEnabled(False)
            self.compressChkBx.setEnabled(False)
            self.progressbar.reset()
            self.progressbar.setHidden(False)
            createFolder(str(self.out_directory.text()))
            self.processFile()
        else:
            self.stop_process = True

    def processFile(self):
        """
        converting images
        :return:
        """
        files = glob.glob(self.in_directory.text())
        compress = self.compressChkBx.isChecked()
        outpath = self.out_directory.text()
        for f in files:
            self.detail.insertPlainText(f)
            self.detail.moveCursor(QTextCursor.End)
            QApplication.processEvents()
            prefix = os.path.basename(f).rsplit('.', 1)[0]

            self.generate_tiff_files(f, outpath, prefix, compress)

        QApplication.restoreOverrideCursor()
        self.detail.moveCursor(QTextCursor.End)
        self.detail.insertPlainText("\nDone. All result images have been saved to "+outpath)
        QApplication.processEvents()
        self.start_button.setChecked(False)
        self.start_button.setText('Start')
        self.in_directory.setEnabled(True)
        self.select_in_folder.setEnabled(True)
        self.out_directory.setEnabled(True)
        self.select_out_folder.setEnabled(True)
        self.compressChkBx.setEnabled(True)

    def log_progress(self, progress, total):
        """
        Print the progress in the terminal
        :param progress, total:
        :return: -
        """
        per = int(progress * 100 / total)
        self.progressbar.setValue(per)
        QApplication.processEvents()
        print('\r[{1:>3}%  {0:40}]'.format('#' * int(40*per/100), per), end='')
        if per >= 100:
            print(' [DONE]')

    def generate_tiff_files(self, fn, path, prefix, compress):
        """
        Generate tiff files from a hdf file.
        :param fn, metadata, path, prefix:
        :return: -
        """
        self.detail.insertPlainText('\nGenerating TIFF Files...')
        self.detail.moveCursor(QTextCursor.End)
        QApplication.processEvents()
        print('Generating TIFF Files...')
        with fabio.open(fn) as fabio_img:
            # create_tiff(fabio_img.data, metadata, path, prefix, 1)
            create_tiff(fabio_img, path, prefix, 1, compress)
            if fabio_img.nframes > 1:
                for i in range(2, fabio_img.nframes + 1):
                    if self.stop_process:
                        break
                    fabio_img = fabio_img.next()
                    # create_tiff(fabio_img.data, metadata, path, prefix, i)
                    create_tiff(fabio_img, path, prefix, i, compress)
                    self.log_progress(i, fabio_img.nframes)
        self.progressbar.setValue(100)
        self.detail.insertPlainText('\n------------------------------ Completed ------------------------------')
        self.detail.moveCursor(QTextCursor.End)
        self.stop_process = False
        QApplication.processEvents()
        print('Completed')

def create_tiff(img_data, path, prefix, serial, compress):
    """
    Create a tiff file from a hdf file.
    :param img_data, metadata, path, prefix, serial:
    :return: -
    """
    tif_file_name = path + os.sep + prefix + '_{:04d}'.format(serial) + '.tif'
    cmp_tif_file_name = path + os.sep + prefix + '_{:04d}'.format(serial) + '_cmp' + '.tif'
    # extra_tags = [("ImageDescription", 's', 0, metadata, True)]
    # tifffile.imsave(tif_file_name, img_data, extratags=extra_tags)
    data = img_data.data.astype(np.int32)
    data[data==4294967295] = -1
    if compress:
        tif_img = Image.fromarray(data)
        tif_img.save(cmp_tif_file_name, compression='tiff_lzw', exif=img_data.getheader())
    else:
        tif_img = fabio.pilatusimage.pilatusimage(data=data, header=img_data.getheader())
        tif_img.write(tif_file_name)

def read_meta_data(meta_fn):
    """
    Read the meta data.
    :param meta_fn: filename where the metadata is stored
    :return: metadata
    """
    with open(meta_fn) as meta:
        return meta.read()
