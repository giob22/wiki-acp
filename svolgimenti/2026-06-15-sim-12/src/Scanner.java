public class Scanner {

    public static void main(String[] args) {
        ProxySorting proxy = new ProxySorting(Integer.valueOf(args[0]));

        for(int i = 0; i < 10; i++){
            String codice = Integer.toString(i);
            double peso = Math.random() * 30.0;

            proxy.smista(codice, peso);

            

        }
    }

}
