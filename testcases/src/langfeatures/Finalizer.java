package langfeatures;

public class Finalizer {

    public static void main(String[] args)
    {
        Finalizer f = new Finalizer(42);

        f.message();

        f = new Finalizer(5);

        f.message();

        f = null;

        System.gc();

        for (int i = 0; i < 3; i++) {
            try {
                System.out.printf("Wait %d/3%n", i+1);
                Thread.sleep(1000);
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }

    public int x;

    public Finalizer(int x)
    {
        this.x = x;
    }

    public void message()
    {
        if (x < 10) {
            System.out.println("less than 10");
        } else {
            System.out.println("more than 10");
        }
    }

    @Override
    public void finalize()
    {
        System.out.println("Finalizing " + this.getClass().getSimpleName());
    }
}