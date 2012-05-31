class Stitch {
  public int yOffset = 0;
  public int xOffset = 0;
  public int w;
  public int h;
  
  public int relX;
  public int relY;
  
  PImage stitchImage;
  
  //Since each stitch is different, they all have different offsets fot X and Y
  int [][] xOffsets = {  
  {0,0,0,0}, //1
  {2,1,1,0}, //2
  {1,1,1,0}, //3
  {1,2,0,0}, //4
  {2,0,1,0}, //5
  {0,1,0,0}, //6
  {0,1,1,0}, //7
  {1,1,1,0}, //8
  {0,0,1,0}, //9
  {0,0,0,0}  //10  
  };
  
  int [][] yOffsets = {  
  //{1,2,1,2},  //0
  {5,5,6,6}, //1
  {5,5,5,5}, //2
  {6,6,6,5}, //3
  {6,5,6,5}, //4
  {5,6,5,5}, //5
  {5,6,5,5}, //6
  {4,7,5,6}, //7
  {4,4,6,7}, //8
  {5,4,4,5}, //9    
  {5,5,5,5}
  };
  
  
  Stitch(int row, int col, String path){
    
    stitchImage = loadImage(path);
    w = stitchImage.width;
    h = stitchImage.height;
    
    xOffset = xOffsets[row][col];
    yOffset = yOffsets[row][col];
  }
  
}
