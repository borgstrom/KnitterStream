/*

This script applies a knitted texture to an image.
To use, place an image into Source folder and change "imageName" to the file you want to convert.
Launch the script and you'll get the result in "Converted" folder.

The texture is based on Joel Glovier's texture. http://dribbble.com/shots/382725-Knit-Pray-Love and there's some room for imporvement when it comes to tiling the texture.
Right now, it's not a 1x1 ratio, so the pattern has to be stretched vertically, which decreases type legibility, especially if it's a pixel font.


Cheers, 
Ivan Sharko 
www.moveplaycreate.com

*/


void setup(){

  String imageSource = "Source/";
  String imageName = "knit.jpeg";
  
  
  size(90,438);
//  background(#ff7800);
   
  PImage piggies;
  PImage myImage = loadImage(imageSource + imageName);
  size(myImage.width, myImage.height);
  image(myImage, 0, 0);
  
  KnittingPattern myPattern = new KnittingPattern();
  myPattern.init(imageName);
}

