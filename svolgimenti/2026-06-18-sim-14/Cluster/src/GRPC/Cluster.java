package GRPC;

import GRPC.Proto.*;
import GRPC.Proto.ClusterGrpc.ClusterImplBase;
import io.grpc.*;
import io.grpc.Context;
import io.grpc.stub.StreamObserver;

import static io.grpc.MethodDescriptor.newBuilder;

import java.io.IOException;
import java.util.Hashtable;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

import javax.jms.*;
import javax.naming.*;

public class Cluster extends ClusterImplBase {


    private TopicConnection topicConnection;
    private Topic gpuTopic;
    private Topic rtTopic;


    public Cluster(TopicConnection topicConnection, Topic gpuTopic, Topic rtTopic) {
        this.topicConnection = topicConnection;
        this.gpuTopic = gpuTopic;
        this.rtTopic = rtTopic;
    }

    public static void main(String[] args){

        Hashtable<String,String> prop = new Hashtable<>();

        prop.put("java.naming.factory.initial", "org.apache.activemq.jndi.ActiveMQInitialContextFactory");
        prop.put("java.naming.provider.url", "tcp://127.0.0.1:61616");

        prop.put("topic.rt", "rt");
        prop.put("topic.gpu", "gpu");
        
        
        try {
            InitialContext jndi_context = new InitialContext(prop);

            // prendo i tre administered objects

            TopicConnectionFactory topicConnectionFactory = (TopicConnectionFactory)jndi_context.lookup("TopicConnectionFactory");

            Topic gpuTopic = (Topic) jndi_context.lookup("gpu");
            Topic rtTopic = (Topic) jndi_context.lookup("rt");

            // creo la connection

            TopicConnection topicConnection = topicConnectionFactory.createTopicConnection();

            // questa connection andrà ad ogni thread che genererò

            // PARTE GRPC
            
            ExecutorService executor = Executors.newFixedThreadPool(10);
            
            
            
            Cluster ClusterImpl = new Cluster(topicConnection, gpuTopic,rtTopic);
            Server server = Grpc.newServerBuilderForPort(50051, InsecureServerCredentials.create())
            .executor(executor)
            .addService(ClusterImpl)
            .build();

            
            
            server.start();

            System.out.println("[SERVER] server is listening on localhost:" + server.getPort());
                
            server.awaitTermination();

            ClusterImpl.close();


        } catch (IOException e) {
            e.printStackTrace();
        } catch (InterruptedException e) {
            e.printStackTrace();
        } catch (NamingException e) {
            e.printStackTrace();
        } catch (JMSException e) {
            e.printStackTrace();
        }

        

    }

    public void close(){
        try {
            this.topicConnection.close();
        } catch (JMSException e) {
            e.printStackTrace();
        }
    }

    @Override
    public void deploy(DeployRequest request, StreamObserver<Ack> responseObserver) {

        WorkerThread workerThread = new WorkerThread(request, this.topicConnection, this.rtTopic, this.gpuTopic, true);

        workerThread.start();

        try {
            workerThread.join();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        
        
        responseObserver.onNext(Ack.newBuilder().setStatus("OK").build());
        responseObserver.onCompleted();
    
    }

    @Override
    public void stopAll(StopRequest request, StreamObserver<Ack> responseObserver) {
        WorkerThread workerThread = new WorkerThread(request, this.topicConnection, this.rtTopic, this.gpuTopic, false);

        workerThread.start();

        try {
            workerThread.join();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        
        
        responseObserver.onNext(Ack.newBuilder().setStatus("OK").build());
        responseObserver.onCompleted();
    }



}
