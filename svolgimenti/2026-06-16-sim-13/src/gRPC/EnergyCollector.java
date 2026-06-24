package gRPC;

import java.io.IOException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

import JMS.EnergyCollectorImpl;
import io.grpc.*;

public class EnergyCollector {

    public static void main(String[] args){

        int port = 50051;
        ExecutorService executor = Executors.newFixedThreadPool(2);

        EnergyCollectorImpl serverImpl = new EnergyCollectorImpl();
    
        Server server = Grpc.newServerBuilderForPort(port, InsecureServerCredentials.create())
                                                .executor(executor)
                                                .addService(serverImpl)
                                                .build();

        try {
            server.start();

            System.out.println("Server is listening on localhost:" + port);

            server.awaitTermination();
            serverImpl.close();


        } catch (IOException e) {
            e.printStackTrace();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }



    }





}
