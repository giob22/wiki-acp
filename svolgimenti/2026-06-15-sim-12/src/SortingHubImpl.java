

public class SortingHubImpl extends SkeletonSorting {

    public static void main(String[] args) {
        SortingHubImpl server = new SortingHubImpl(0);
        server.run_skeleton();
    }

    public SortingHubImpl(int port) {
        super(port);
    }

    @Override
    public synchronized void smista(String codice, double peso) {

        String zona = null;

        if (peso <= 5.0) {
            zona = "standard";
        }else if (peso > 5.0 && peso <=20.0){
            zona = "pesante";
        }else{
            zona = "eccezionale";
        }

        ThreadSorting thread = new ThreadSorting(codice, peso, zona);
        thread.start();
        System.out.println("threadSorting avviato");
    }

}
