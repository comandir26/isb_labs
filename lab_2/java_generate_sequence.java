import java.util.Random;

public class Main
{
	public static void random(int size) {
		Random rand = new Random();
        for(int i = 0; i < 128; i++) {
            System.out.print(rand.nextInt(2));
        }
	}
	
	public static void main(String[] args) {
		random(128);
	}
}
