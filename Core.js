import org.opencv.core.*;
import org.opencv.imgcodecs.Imgcodecs;
import org.opencv.imgproc.Imgproc;

public class OpenCVExample {
static { System.loadLibrary(Core.NATIVE_LIBRARY_NAME); }

public static void main(String[] args) {
Mat image = Imgcodecs.imread("data/image.jpg");
Imgproc.cvtColor(image, image, Imgproc.COLOR_BGR2GRAY);
Imgcodecs.imwrite("data/gray_image.jpg", image);
}
}
