# watermark
Python script to add text watermark to images.

# How to use
First install dependencies: python3, pillow and pysimplegui.

watermark_files.py opens a file dialog so you can select one or more files to apply the watermark.

watermark_dir.py is a command line utility to apply watermark to all images in a specified folder.

Before using either of these two, edit them. You will see at the necessary configuration at file beginning. 
You will need to configure the watermark text. 
In watermark_dir.py you will also need to configure source and destination directories.
Both files use the font contained here, but you may provide your own.

# Note
The /home/rada/Projects/watermark/watermark_dir.py was tested only on linux, but the watermark_files.py was tested on Linux and Win10.
