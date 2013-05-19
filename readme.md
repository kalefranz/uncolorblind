<div align="center"><img src="https://raw.github.com/kalefranz/uncolorblind/master/aux/screenshot.png" alt="screen shot" width="399" height="258"></div>

## uncolorblind app ##

This is a little app especially designed for people, like me, who are color blind.  It has a lot of the same
functionality as [DigitalColor Meter](http://en.wikipedia.org/wiki/DigitalColor_Meter) on OS X…with one twist.
It will tell you the *name* of the color along with the RGB values. Given the RGB values of the pixel under the
mouse pointer, it does a simple regression to find the closest match to the
[X11 color names](http://en.wikipedia.org/wiki/Web_colors).  And it gives both the X11 color name and the "group name"
as categorized on the [wikipedia page](http://en.wikipedia.org/wiki/Web_colors).

For color blind people, having the actual names of the colors is immensely helpful.  And if you're not color blind,
I'm guessing this utility might still be useful.  Even though I *am* color blind, I'm pretty decent at telling people
what RGB values a color might be, just by eye. (Yeah, so not the R part of RGB *as much*, since that's where my eyes
let me down.)  But really, with a little use it's pretty easy to gain intuition about color => RGB mapping.

The script is written in python using the Qt framework, so it should work on OS X, Windows, and Linux alike.
At some point, once the code is mature, I'll package up some binaries and post them on [Bintray](https://bintray.com)
or the like.