# Dillinger
## _The Last Markdown Editor, Ever_

[![N|Solid](https://cldup.com/dTxpPi9lDf.thumb.png)](https://nodesource.com/products/nsolid)

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

Dillinger is a cloud-enabled, mobile-ready, offline-storage compatible,
AngularJS-powered HTML5 Markdown editor.

- Type some Markdown on the left
- See HTML in the right
- ✨Magic ✨

## Features

- Import a HTML file and watch it magically convert to Markdown
- Drag and drop images (requires your Dropbox account be linked)
- Import and save files from GitHub, Dropbox, Google Drive and One Drive
- Drag and drop markdown and HTML files into Dillinger
- Export documents as Markdown, HTML and PDF

Markdown is a lightweight markup language based on the formatting conventions
that people naturally use in email.
As [John Gruber] writes on the [Markdown site][df1]

> The overriding design goal for Markdown's
> formatting syntax is to make it as readable
> as possible. The idea is that a
> Markdown-formatted document should be
> publishable as-is, as plain text, without
> looking like it's been marked up with tags
> or formatting instructions.

This text you see here is *actually- written in Markdown! To get a feel
for Markdown's syntax, type some text into the left window and
watch the results in the right.

## Tech

Dillinger uses a number of open source projects to work properly:

- [AngularJS] - HTML enhanced for web apps!
- [Ace Editor] - awesome web-based text editor
- [markdown-it] - Markdown parser done right. Fast and easy to extend.
- [Twitter Bootstrap] - great UI boilerplate for modern web apps
- [node.js] - evented I/O for the backend
- [Express] - fast node.js network app framework [@tjholowaychuk]
- [Gulp] - the streaming build system
- [Breakdance](https://breakdance.github.io/breakdance/) - HTML
to Markdown converter
- [jQuery] - duh

And of course Dillinger itself is open source with a [public repository][dill]
 on GitHub.

## Installation

Dillinger requires [Node.js](https://nodejs.org/) v10+ to run.

Install the dependencies and devDependencies and start the server.

```sh
cd dillinger
npm i
node app
```

For production environments...

```sh
npm install --production
NODE_ENV=production node app
```

## Plugins

Dillinger is currently extended with the following plugins.
Instructions on how to use them in your own application are linked below.

| Plugin | README |
| ------ | ------ |
| Dropbox | [plugins/dropbox/README.md][PlDb] |
| GitHub | [plugins/github/README.md][PlGh] |
| Google Drive | [plugins/googledrive/README.md][PlGd] |
| OneDrive | [plugins/onedrive/README.md][PlOd] |
| Medium | [plugins/medium/README.md][PlMe] |
| Google Analytics | [plugins/googleanalytics/README.md][PlGa] |

## Development

Want to contribute? Great!

Dillinger uses Gulp + Webpack for fast developing.
Make a change in your file and instantaneously see your updates!

Open your favorite Terminal and run these commands.

First Tab:

```sh
node app
```

Second Tab:

```sh
gulp watch
```

(optional) Third:

```sh
karma test
```

#### Building for source

For production release:

```sh
gulp build --prod
```
# Parking camera system VW Golf 2017 - (BirdEye)

## _equimpent to prepare:_

 - (4) ELP 8mp USB Camera Wide Angle Fisheye Lens 185 Degree 4K [amazon](https://www.amazon.com/-/he/dp/B01HD1V3UO?ref=ppx_yo2ov_dt_b_product_details&th=1)
 - (4) papers of checkboard white-black (5X5), size 100cmX100cm the size of each black/white square is 20cmX20cm.


# camera calibration:
	
1. connect the camera to the pc and capture multiple images of the checkerboard pattern from different angles and positions.
	examples exists in [cameraCalbiration\imgs](https://github.com/majedabu/Parking-Camera-System/tree/main/cameraCalbiration/imgs)
script : [CaptureAndSave.html](https://github.com/majedabu/Parking-Camera-System/blob/main/cameraCalbiration/CaptureAndSave.html)

|   |   |   |
|:-:|:-:|:-:|
|ex1|ex2|ex3|
|<img style="margin:0px auto;display:block" width=250 src=".\cameraCalbiration\imgs\captured_image (35).png"/>|<img style="margin:0px auto;display:block" width=250 src=".\cameraCalbiration\imgs\captured_image (23).png"/>|<img style="margin:0px auto;display:block" width=250 src=".\cameraCalbiration\imgs\captured_image (19).png"/>|
 \
2. calbirate the camera  using OpenCV calibration method for fisheye cameras.\
script : [extractFisheyeCameraIntrinsics.py](https://github.com/majedabu/Parking-Camera-System/blob/main/cameraCalbiration/extractFisheyeCameraIntrinsics%20.py)

|   |
|:-:|
|camera matrix output (focal length and center) + Distortion Coefficients|
|<img style="margin:0px auto;display:block" width=250 src=".\cameraCalbiration\imgs\captured_image (35).png"/>|
\
# image undistortion
