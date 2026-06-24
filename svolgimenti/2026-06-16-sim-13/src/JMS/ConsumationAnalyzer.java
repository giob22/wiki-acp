package JMS;

import java.util.Hashtable;

import javax.jms.*;
import javax.naming.*;

public class ConsumationAnalyzer {

    public static void main(String[] args){
        // INIZIALIZZO JMS

        Hashtable<String,String> prop = new Hashtable<>();

        prop.put("java.naming.factory.initial", "org.apache.activemq.jndi.ActiveMQInitialContextFactory");
        prop.put("java.naming.provider.url", "tcp://127.0.0.1:61616");

        prop.put("queue.energy", "energy");


        // context
        try {
            Context jndi_context = new InitialContext(prop);
            
            // administered objects
            QueueConnectionFactory queueConnectionFactory = (QueueConnectionFactory) jndi_context.lookup("QueueConnectionFactory");
            
            Queue queue = (Queue)jndi_context.lookup("energy");
            
            // creo la connection
            
            QueueConnection conn = queueConnectionFactory.createQueueConnection();

            // attivo la ricezione sulla connessione

            conn.start();

            // creo la sessione

            Session session = conn.createSession(false, Session.AUTO_ACKNOWLEDGE);

            // creo il receiver

            MessageConsumer receiver = (MessageConsumer) session.createConsumer(queue);

            receiver.setMessageListener(new ConsumationListener());

            Thread.currentThread().join();

            receiver.close();
            session.close();
            conn.close();

        
        } catch (NamingException e) {
            e.printStackTrace();
        } catch (JMSException e) {
            e.printStackTrace();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

    }

}
