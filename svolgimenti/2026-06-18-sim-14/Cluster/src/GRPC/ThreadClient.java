package GRPC;



public class ThreadClient extends Thread{

    private Client client;
    private int name_t;
    public ThreadClient(Client client, int name){
        this.name_t = name;
        this.client = client;
    }


    @Override
    public void run() {


        for (int i = 0; i < 4; i++){
            int id = (int)(Math.round((Math.random() * 10)));
            int tmp = (int)  Math.round((Math.random() * 2));

            
            String name = "Client" + this.name_t;

            String type = (tmp == 1) ? "gpu-bound" : "real-time";
            

            System.out.println("richiesta di deploy per: " + id + "|" + name + "|" + type);



            this.client.deploy(id,name,type);

            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }

            
        }
        int tmp = (int)  Math.round((Math.random() * 2));    

        String type = (tmp == 1) ? "gpu-bound" : "real-time";

        this.client.stop_all(type);
        
        
    }

}
