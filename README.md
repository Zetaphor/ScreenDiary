### Process

* Take a screenshot every 2 seconds
* Check the image for a transparent boundary (this is from Spectacle)
  * If found, replace the transparency with `TRANSPARENCY_REPLACEMENT_COLOR`
  * Then crop the image to remove the boundary, accounting for drop shadows with `TRANSPARENCY_COLOR_THRESHOLD`
* Determine if the image has a titlebar by checking for the `TITLEBAR_COLOR` at `TITLEBAR_COLOR_X`, `TITLEBAR_COLOR_Y`
  * If a titlebar is found, crop the titlebar using `TITLEBAR_HEIGHT`, cutting off the left and right sides using `TITLEBAR_LEFT_BOUNDARY` and `TITLEBAR_RIGHT_BOUNDARY` to remove the window, icon and window decorations.
  * Run OCR on the window titlebar
* Run OCR on the window contents