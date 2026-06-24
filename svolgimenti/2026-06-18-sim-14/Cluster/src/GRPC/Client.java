package GRPC;

import java.util.concurrent.TimeUnit;

import GRPC.Proto.*;
import GRPC.Proto.ClusterGrpc.*;
import io.grpc.*;




public class Client {
    
    private ClusterBlockingStub stub;
    private final int N_THREAD = 5;
    
    public Client(Channel channel){
        this.stub = ClusterGrpc.newBlockingStub(channel);
        
    }

    public static void main(String[] args){

        ManagedChannel channel = Grpc.newChannelBuilder("localhost:50051", InsecureChannelCredentials.create()).build();

        Client client = new Client(channel);

        client.start();

        try {
            channel.shutdownNow().awaitTermination(5, TimeUnit.SECONDS);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

    }

    public void start(){
        ThreadClient[] threads = new ThreadClient[N_THREAD];
        for (int i = 0; i < N_THREAD; i++){
            threads[i] = new ThreadClient(this, i);
            threads[i].start();
        }
        for (int i = 0; i < N_THREAD; i++){
            try {
                threads[i].join();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }

    public void deploy(int id, String name, String type){

        DeployRequest request = DeployRequest.newBuilder().setId(id).setName(name).setType(type).build();

        Ack ack = this.stub.deploy(request);

        System.out.println("Esito del deploy: " + ack.getStatus());

    }

    public void stop_all(String type){

        StopRequest request = StopRequest.newBuilder().setType(type).build();

        Ack ack = this.stub.stopAll(request);

        System.out.println("Stopped all " + type + " tasks. " + ack.getStatus());

    }


}
