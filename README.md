# AirSwipe

AirSwipe is a gesture-controlled desktop automation system that enables cursor control, scrolling, presentation navigation, copy-paste operations, zooming, brightness adjustment, and volume control through real-time hand tracking.

## Overview

The project uses computer vision and hand landmark detection to recognize predefined gestures and map them to system actions. By eliminating the need for traditional input devices for certain tasks, AirSwipe demonstrates how gesture recognition can be applied to improve accessibility, productivity, and human-computer interaction.

## Features

* Cursor movement using hand gestures
* Gesture-based scrolling
* PowerPoint slide navigation
* Copy and paste actions
* Zoom controls
* Window minimize and maximize functionality
* System volume control
* System brightness control
* Interactive launcher dashboard for accessing different gesture modules

## Technologies Used

* Python
* OpenCV
* MediaPipe
* PyAutoGUI
* Tkinter
* PyCAW

## How It Works

AirSwipe uses MediaPipe's hand tracking capabilities to detect hand landmarks in real time through a webcam feed. These landmarks are processed to identify specific gestures, which are then mapped to corresponding desktop actions such as scrolling, clicking, zooming, navigating presentations, or controlling system settings.

The project is divided into multiple modules, allowing different gesture-based functionalities to be launched independently through a centralized dashboard.

## Demo

A demonstration video is included in this repository, showcasing the different gesture-based controls implemented in the project.
A demonstration of the project can be viewed here:

**Google Drive Link**:
https://drive.google.com/file/d/1aTF7ULsItt7P0hDyj4zzW-5Y45fy-zum/view?usp=sharing

## Future Improvements

* Support for additional custom gestures
* Improved gesture accuracy and stability
* Cross-platform compatibility enhancements
* Gesture customization through a settings interface
* Integration with more desktop applications

```
```
