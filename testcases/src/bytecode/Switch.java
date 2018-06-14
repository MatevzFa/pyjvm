package bytecode;

public class Switch {

    public static void main(String[] args) {
        int a = 123;

        switch(a) {
            case 1: a = a + 9*a; break;
            case 2: a = a + 8*a; break;
            case 3: a = a + 7*a; break;
            case 4: a = a + 6*a; break;
            case 5: a = a + 5*a; break;
            case 6: a = a + 4*a; break;
            case 123: a = a + 3*a; break;
            default: a = a + 2*a;
        }

        System.out.println(a == 123 + 3 * 123);
    }
}