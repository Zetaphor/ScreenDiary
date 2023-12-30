# ScreenDiary

A tool to keep a visual and text log of everything you've done with your computer, allowing you to easily search through your previous activity.

See the `.env` file for configuration.

### Image Processing Pipeline

* Take a screenshot every 2 seconds
* Check if the current image is different from the previous image (perceptual hashing)
* Extract the titlebar content using tesseract OCR
  * This is done by scanning downward from the `TITLEBAR_COLOR_X, 0` coordinates of the screenshot for the presence of the `TITLEBAR_COLOR`, and then cropping from that point down to the `TITLEBAR_HEIGHT`
  * The titlebar is then further cropped using the `TITLEBAR_LEFT_BOUNDARY` and `TITLEBAR_RIGHT_BOUNDARY` to remove the window icon and window decorations
  * If we've passed the `TITLEBAR_COLOR_Y_LIMIT` without finding the color, the screenshot does not have a titlebar
* Extract the text content using tesseract OCR