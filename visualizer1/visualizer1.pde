int n;
int f;
int FOV;
float interval;
float[][] sectors;
float[][] target_z;
float[][] motion;
float[] dimensions;
void setup() {
  size(700,700,P3D);
  background(0);
  lights();
  n = 10;
  interval = 1;
  dimensions = new float[]{width/(interval*n), height/(interval*n)};
  sectors = new float[n][n];
  motion = new float[n][n];
  target_z = new float[n][n];
  for (int i = 0; i < n; i++) {
    for (int j = 0; j < n; j++) {
      sectors[i][j] = 10;
    }
  }
  f = 0;
  FOV = 900;
  max_motion = 0;
  noStroke();
}
Table table;
float max_motion;
void draw() {
  // read input motion values
  if (f % 10 == 0) {
    table = loadTable("foo.csv");
    
    max_motion = 0;
    for (int i = 1; i < n; i++) {
       for (int j = 1; j < n; j++) {
         try {
           motion[i][j] = Float.parseFloat(table.getString(i, j));
         } catch (ArrayIndexOutOfBoundsException e) {
            continue;
         }
         if (motion[i][j] > max_motion)
           max_motion = motion[i][j];
       }
    }
  }
  
  clear();
  
  for (int i = 1; i < n; i++) {
    for (int j = 1; j < n; j++) {
      float colorScale = sectors[i][j] / FOV;
      fill(colorScale * 255, colorScale * 50, colorScale * 167);
      
      pushMatrix();
      translate(interval*i*dimensions[0], interval*j*dimensions[1], -400);
      //rotateZ(f*PI/100);
      //rotateY((f%100)*PI/100);
      box(dimensions[0], dimensions[1], sectors[i][j]);
      popMatrix();
      
      target_z[i][j] = (motion[i][j] / max_motion) * FOV;
      float scale = 1 + (target_z[i][j]-sectors[i][j])/(50*sectors[i][j]);
      sectors[i][j] *= scale;
    }
  }
  f++;
}