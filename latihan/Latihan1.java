package latihan;

public class Latihan1 {
    public static void showMyProfile() {
        String nama = "Gede Ardi Pratama";
        String alamat = "Jakarta Selatan";
        int umur = 22;
        System.out.println("Nama: " + nama);
        System.out.println("Alamat: " + alamat);
        System.out.println("Umur: " + umur);
    }

    public static void operators() {
            int a = 12, b = 5;
            System.out.println("a + b = " + (a + b));

            System.out.println("a - b = " + (a - b));
            System.out.println("a * b = " + (a * b));
            System.out.println("a / b = " + (a / b));
            System.out.println("a % b = " + (a % b));
    }
    public static void registered() {
        boolean isRegistered = true;
        if (isRegistered) {
            System.out.println("Sudah terdaftar");
        } else {
            System.out.println("Tidak terdaftar");
        }
    }
    public static void loopingFor() {
        int angka = 2;
        for (int i = 1; i <= 6; i++) {
            System.out.print(angka + " ");
            if (i < 4) {
                angka += 2;
            } else {
                angka *= 2;
            }
        }
        System.out.println("Penerapan For");
    }
    public static void loopingWhile() {
        int a = 2, b = 4;
        System.out.print(a + " " + b + " ");
        int i = 3;
        while (i <= 5) {
            int next = a * b;
            System.out.print(next + " ");
            a = b;
            b = next;
            i++;
        }
        System.out.println("Penerapan While");

    }
    public static void urutAngka()
    {
        int[] numbers = {6, 6, 5, 9, 2};
        for (int i = 0; i < numbers.length - 1; i++) {
            for (int j = 0; j < numbers.length - 1 - i; j++) {
                if (numbers[j] < numbers[j + 1]) {
                    int temp = numbers[j];
                    numbers[j] = numbers[j + 1];
                    numbers[j + 1] = temp;
                }
            }
        }
        System.out.print("Urutan dari besar ke kecil: ");
        for (int num : numbers) {
            System.out.print(num + " ");
        }
        System.out.println();
    }
    public static void polaBlooping()
    {
        int a = 2;
        int b = 4;
        System.out.print(a + " " + b + " ");
        int i = 3;
            while (i <= 5) {
                int next;
                if (i == 5) {
                    next = 216;
                } else {
                    next = a * b;
                }

                    System.out.print(next + " ");
                    a = b;
                    b = next;
                    i++;
                }

                System.out.println();
            }
    public static void urutAbjad()
    {
        char[] abjad = {'M', 'A', 'K', 'A', 'N', 'N', 'A', 'S', 'I'};
        for (int i = 0; i < abjad.length - 1; i++) {
            for (int j = 0; j < abjad.length - 1 - i; j++) {
                if (abjad[j] > abjad[j + 1]) {
                    char temp = abjad[j];
                    abjad[j] = abjad[j + 1];
                    abjad[j + 1] = temp;
                }
            }
        }
        System.out.print("Urutan abjad dari awal ke akhir: ");
        for (char letter : abjad) {
            System.out.print(letter + " ");
        }
        System.out.println();
    }
    public static void mathImplemen() {
        System.out.println(Math.round(4.6));
        System.out.println(Math.floor(4.9));
    }
    public static void fizzBuzz()
    {
        for (int i = 1; i <= 20; i++) {
            if (i % 3 == 0 && i % 5 == 0) {
                System.out.println("Fizz Buzz");
            }
            else if (i % 3 == 0) {
                System.out.println("Fizz");
            }
            else if (i % 5 == 0) {
                System.out.println("Buzz");
            }
            else {
                System.out.println(i);
            }
        }
    }
    public static void main(String[] args) {
       operators();
       showMyProfile();
       registered();
        loopingFor();
        loopingWhile();
        urutAngka();
        urutAbjad();
        polaBlooping();
        mathImplemen();
        fizzBuzz();
    }
}