/*

 Knitting pattern turns whatever is drawn in the sketch into an imitation of a knitted piece.
 It is done by recreating each pixel of the image as a "stitch". The knitting texture consists of a tiled texture 4x10 stitches. Each of which,
 gets colored according to pixels[] array of the original sketch drawing.
 
 */
class KnittingPattern {

  import java.awt.Color;
  PGraphics buf;

  //Where are we saving the image that was generated and what's the index?
  //patternIndex is used for saving more than one image out of this class.
  int patternIndex = 0;
  String stitchPatternPath = "data/StitchPattern/";
  String patternSavePath = "data/Converted/";

  //Main offset of the big knitted image that's going to be drawn in the buffer
  int _offsetX = 0;
  int _offsetY = 0;
  
  String imageName;

  //Knitting texture
  ArrayList <Stitch[]> knitTexture = new ArrayList ();


  //------------------------------------------------------------------------------------------------------------------------------------
  //CONSTRUCTOR-----------------------------------------------
  KnittingPattern() {

    //Init knit texture.
    knitTexture.add(new Stitch [4]); 
    knitTexture.add(new Stitch [4]);
    knitTexture.add(new Stitch [4]);
    knitTexture.add(new Stitch [4]);
    knitTexture.add(new Stitch [4]);
    knitTexture.add(new Stitch [4]);
    knitTexture.add(new Stitch [4]);
    knitTexture.add(new Stitch [4]);
    knitTexture.add(new Stitch [4]);
    knitTexture.add(new Stitch [4]);


    // go through rows/cols to init each Stitch in the pattern
    for (int row=0; row < knitTexture.size(); row ++) {        
      for (int col=0; col < knitTexture.get(row).length; col ++) {
        String path = stitchPatternPath + (row+1) + "-" + (col+1) + ".png";                
        knitTexture.get(row)[col] = new Stitch(row, col, path);
      }
    }

    // go through rows/cols to setup relative X position of each stitch and account for xOffsets that are unique to each stitch
    for (int row=0; row < knitTexture.size(); row ++) {
      int myX = 0;
      for (int col=0; col < knitTexture.get(row).length; col ++) {        
        knitTexture.get(row)[col].relX = myX;        
        myX += knitTexture.get(row)[col].stitchImage.width;
        myX -= knitTexture.get(row)[col].xOffset;
      }
    }

    // go through cols/rows to setup relative Y position of each stitch and account for yOffsets that are unique to each stitch
    for (int col=0; col < 4; col ++) {        
      int myY = 0;
      for (int row=0; row < knitTexture.size(); row ++) {
        knitTexture.get(row)[col].relY = myY;
        myY += knitTexture.get(row)[col].stitchImage.height;
        myY -= knitTexture.get(row)[col].yOffset;
      }
    }
  }


  //------------------------------------------------------------------------------------------------------------------------------------
  //Init the converter by loading pixels in the sketch and initializing the buffer based on the sketch height and width.
  void init(String _imageName) {    
    imageName = _imageName;
    int bufHeight = floor(height*7);
    buf = createGraphics(width * 10, bufHeight, P2D);
    generate();
  }

  //------------------------------------------------------------------------------------------------------------------------------------
  //Generate stitch pattern and draw it into the buffer
  void generate() {
    smooth();
    int x, y, row, col;
    int chunkX, chunkY;
    int indexX, indexY;
    int yOffset = 0;

    loadPixels();

    //Begin drawing the texture into buffer    
    buf.beginDraw();
    //    buf.image(bgTexture, 0, 0);

    //Cycyle through "pixels" array and create a "stitch" for every pixel in the buffer.
    for (int i=0; i < pixels.length; i++) {
      //find out which row and column we are on, based one a 1-dimensional pixels array
      row = i/width;
      col = i%width;

      //how many WHOLE chunks have we already drawn? This will affect our offsets
      chunkX = col/4;
      chunkY = row/10;

      //Which row and column of a tiled pattern (knitted pattern chunk) are we drawing?
      indexX = (col-chunkX*4)%4;
      indexY = (row-chunkY*10)%10;

      //setup the Stitch and draw it in according position
      Stitch _s = knitTexture.get(indexY)[indexX];
      if (indexX == 0) {
        x = _s.relX +  40 * chunkX + _offsetX + int(random(2));
      } 
      else {
        x = _s.relX +  40 * chunkX + _offsetX;
      }      
      y = _s.relY +  68 * chunkY + _offsetY;

      //TINT the stitch and draw it in the buffer
      buf.tint(pixels[i]);
      buf.image(_s.stitchImage, x, y);
    }

    buf.endDraw();
    
    //Create another buffer.
    //After initial conversion to a pattern, we have to stretch it vertically by 30%, becase the stitches aren't a 1 to 1 ratio. They are thinner and scew the design
    //We also have to up the saturation/levels of the design. This is done by a "saturate" function    
    float scaleY = 1.3;
    PGraphics buf1 = createGraphics(buf.width, int(buf.height*scaleY), JAVA2D);
    buf1.beginDraw();
    buf1.image(buf, 0, 0, buf1.width, buf1.height);    
    saturate(buf1);
    buf1.endDraw();

    //Save the pattern into a folder
    buf1.save(patternSavePath + imageName);
    
    
    //Up the patternIndex, in case we are saving more images from this program in the future
    patternIndex += 1;
  } // end generate
  
  
  //Saturate the design, because simply tinting the stitches makes their colors dull---------------------------------------------------
  void saturate(PGraphics buf1){
    
    buf1.loadPixels();
    for (int x = 0; x < buf1.pixels.length; x++) {
        float r, g, b;
        r = red (buf1.pixels[x]);
        g = green (buf1.pixels[x]);
        b = blue (buf1.pixels[x]);
        //Get RGB Value of each pixel
        if (buf1.pixels[x] != 0){
          //Convert RGB to HSB
          float [] _HSB = new float[3];
          Color.RGBtoHSB(int(r),int(g),int(b), _HSB);
          colorMode(HSB, 100);
          //Increase "Saturation" and "Black" values, making them less dark and more saturated.
          color c = color(_HSB[0]*100,_HSB[1]*100,_HSB[2]*310);
          buf1.pixels[x] = c;
        }
    }
    buf1.updatePixels();
  }
}

