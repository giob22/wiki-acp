package JMS;

import java.util.Hashtable;


import javax.jms.*;
import javax.naming.*;

import gRPC.EnergyService.Reading;
import gRPC.EnergyService.Ack;
import gRPC.EnergyService.EnergyServiceGrpc.EnergyServiceImplBase;
import io.grpc.stub.StreamObserver;

public class EnergyCollectorImpl extends EnergyServiceImplBase{

    private QueueConnection conn;
    private QueueSession session;
    private Queue queue;
    private MessageProducer sender;

    public EnergyCollectorImpl() {

        // INIZIALIZZO JMS

        Hashtable<String,String> prop = new Hashtable<>();

        prop.put("java.naming.factory.initial", "org.apache.activemq.jndi.ActiveMQInitialContextFactory");
        prop.put("java.naming.provider.url", "tcp://127.0.0.1:61616");

        prop.put("queue.energy", "energy");


        try {
            // context
            Context jndi_context = new InitialContext(prop);

            // administered objects
            QueueConnectionFactory queueConnectionFactory = (QueueConnectionFactory) jndi_context.lookup("QueueConnectionFactory");

            this.queue = (Queue)jndi_context.lookup("energy");

            // creo la connection

            this.conn = queueConnectionFactory.createQueueConnection();

            // creo la session

            this.session = this.conn.createQueueSession(false, Session.AUTO_ACKNOWLEDGE);

            // creo il sender

            this.sender = (MessageProducer) this.session.createProducer(queue);
        } catch (NamingException | JMSException e) {
            e.printStackTrace();
        }

    }

    public void close(){
        try {
            this.sender.close();
            this.session.close();
            this.conn.close();
            System.out.println("[SERVER] chiusura completata");
        } catch (JMSException e) {
            e.printStackTrace();
        }
        

    }


    @Override
    public void reportConsumption(Reading request, StreamObserver<Ack> responseObserver) {
        
        String meter_id = request.getMeterId();
        float kwh = request.getKwg();


        // QUI DEVO INSERIRE L'INVIO DEI MESSAGGI TRAMITE JMS

        try {
            TextMessage message = this.session.createTextMessage();

            String text = meter_id+"|"+kwh;

            message.setText(text);

            this.sender.send(message);

   
        } catch (Exception e) {
            e.printStackTrace();
        }    
        
        
        Ack ack = Ack.newBuilder().setStatus("OK").build();

        responseObserver.onNext(ack);
        responseObserver.onCompleted();

        System.out.println("[RECV] meter_id" + meter_id + " kwh=" + kwh);



    }

}
