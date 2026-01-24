#!/bin/bash


SCRIPT_DIR="/home/bill-clinton/RecCode/Python/GnomeTimeWallpaper"


echo "Script launched at $(date)" >> /tmp/wallpaper_script_log.txt


cd "$SCRIPT_DIR"


PYTHON_FILE="backGroundProcess.py"


if [ ! -f "$PYTHON_FILE" ]; then
   
    echo "Error: Python file '$PYTHON_FILE' not found in $SCRIPT_DIR" >> /tmp/wallpaper_script_log.txt
    exit 1
fi

# Execute the Python file
echo "Starting $PYTHON_FILE..." >> /tmp/wallpaper_script_log.txt
python3 "$PYTHON_FILE" &

exit 0
