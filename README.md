# Hand Gesture Paint Application
A real-time drawing application that uses hand gestures detected via MediaPipe to control various drawing tools including line, rectangle, free draw, circle, and eraser.

# Features
Gesture-based tool selection using index finger hover over toolbar

Five drawing tools: Line, Rectangle, Free Draw, Circle, Eraser

Index finger raise detection for drawing activation

Real-time preview of shapes before confirmation

Non-destructive drawing on mask overlay

Visual feedback with hand landmarks and tool indicators

# Requirements
bash
pip install mediapipe opencv-python numpy
# Usage
Place tools.png in the same directory as the script (toolbar image with 5 tools)

Run the script: python paint_app.py

Use hand gestures to interact:

# Tool Selection
Hover index finger (tip 8) over toolbar area (left side of screen)

Hold for 0.8 seconds to select tool

Yellow circle shrinks during selection

# Drawing Controls
Raise index finger (tip 12 above middle finger tip 9 by 40+ pixels) to draw

Lower index finger to confirm/finalize shapes

# Tools
Position	Tool	Behavior
0-50px	Line	Preview line, confirm on finger down
50-100px	Rectangle	Preview rectangle, confirm on finger down
100-150px	Draw	Freehand drawing while finger raised
150-200px	Circle	Preview circle using distance, confirm on finger down
200-250px	Erase	30px circular eraser while finger raised
# Controls
ESC: Exit application

Drawing Area: Main canvas (right side of screen)

Toolbar: Left side (150px margin from left edge)

# Code Structure
python
Key Components
- MediaPipe Hands detection (confidence: 0.6)
- Tool selection via x-coordinate hovering
- Gesture detection: index_raised(yi, y9)
- Mask-based non-destructive drawing
- Real-time shape preview on original frame
# Hand Landmarks Used
8: Index finger tip (tool selection, drawing point)

12: Index finger PIP (gesture detection)

9: Middle finger tip (gesture detection reference)

# Customization
python
ml = 150          # Left margin for toolbar
max_x, max_y = 250 + ml, 50  # Toolbar dimensions
rad = 40          # Selection circle radius
thick = 4         # Drawing thickness
# Troubleshooting
Ensure good lighting and hand visibility

Adjust min_detection_confidence if detection fails

Verify tools.png exists (480x50px recommended)

Camera index 0 may need adjustment for external cameras

# Dependencies
Python 3.7+

MediaPipe 0.10.0+

OpenCV 4.8.0+

NumPy 1.24+
