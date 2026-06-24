package GRPC;

import javax.jms.*;

import com.google.protobuf.GeneratedMessage;

import GRPC.Proto.DeployRequest;
import GRPC.Proto.StopRequest;


public class WorkerThread extends Thread {

    private TopicConnection topicConnection;
    private Topic gpuTopic;
    private Topic rtTopic;
    private GeneratedMessage request;
    private boolean is_deploy;

    public WorkerThread(GeneratedMessage request, TopicConnection topicConnection, Topic gpuTopic, Topic rtTopic, boolean is_deploy) {
        this.request = request;
        this.topicConnection = topicConnection;
        this.gpuTopic = gpuTopic;
        this.rtTopic = rtTopic;
        this.is_deploy = is_deploy;
        
    }


    @Override
    public void run() {

        // inizializzo la session
        
        try {
            TopicSession session = this.topicConnection.createTopicSession(false, Session.AUTO_ACKNOWLEDGE);

            TextMessage textMessage = session.createTextMessage();
            boolean is_gpu = false;
            if (this.is_deploy){
                // DEPLOY

                // UP CAST
                DeployRequest deployRequest = (DeployRequest) this.request;
                
                String text = "DEPLOY-" + deployRequest.getId() + "-" + deployRequest.getName();
                
                textMessage.setText(text);  

                is_gpu = deployRequest.getType().equals("gpu-bound") ? true : false;
                
                System.out.println("Messaggio inviato: DEPLOY-" + deployRequest.getId() + "-" + deployRequest.getName());

            }else {
                // STOP_ALL

                // UP CAST
                StopRequest stopRequest = (StopRequest) this.request;

                String text = "STOP_ALL";

                is_gpu = stopRequest.getType().equals("gpu-bound") ? true : false;

                textMessage.setText(text);

                System.out.println("Messaggio inviato: STOP_ALL");
            }

            if (is_gpu){
                    TopicPublisher publisher = session.createPublisher(gpuTopic);
                    System.out.println("Messaggio inviato su GPU: " + textMessage.getText());
                    publisher.send(textMessage);
            }else{
                    TopicPublisher publisher = session.createPublisher(rtTopic);
                    System.out.println("Messaggio inviato su RT: " + textMessage.getText());
                    publisher.send(textMessage);
            }    
            
            
            
        } catch (JMSException e) {
            e.printStackTrace();
        }

    }




    

    
}
