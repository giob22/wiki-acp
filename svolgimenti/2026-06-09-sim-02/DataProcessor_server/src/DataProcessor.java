import java.util.Hashtable;

import javax.naming.*;
import javax.jms.*;

public class DataProcessor {
    public static void main(String[] args) {
        
        // devo inizializzare il contesto

        Hashtable<String, String> prop = new Hashtable<>();


        prop.put("java.naming.factory.initial", "org.apache.activemq.jndi.ActiveMQInitialContextFactory");
        prop.put("java.naming.provider.url", "tcp://127.0.0.1:61616");

        prop.put("queue.telemetry", "telemetry");

        // creo il contesto su cui farò le chiamate al servizio di naming tramite l'interfaccia JNDI

        try {
            Context context = new InitialContext(prop);
            // ottengo il primo object administered
            QueueConnectionFactory qConnectionFactory = (QueueConnectionFactory)context.lookup("QueueConnectionFactory");
            // ottengo il secondo object administered
            // corrispondente alla coda su cui devo ricevere i messaggi
            
            Queue queue_telematry = (Queue) context.lookup("telemetry");

            
            // creo una connessione 
            QueueConnection qConnection = (QueueConnection) qConnectionFactory.createConnection();

            // starto la connessione perché devo ricevere dei messaggi da essa in modo asincrono
            qConnection.start();

            // creo la sessione
            QueueSession qSession = (QueueSession) qConnection.createSession(false, Session.AUTO_ACKNOWLEDGE);

            // creo il receiver

            QueueReceiver receiver = qSession.createReceiver(queue_telematry);

            // creo il listener per il receiver
            TelematryListener listener = new TelematryListener();

            // setto il listenere sul receiver

            receiver.setMessageListener(listener); 

            System.out.println("Server is listening");


        } catch (NamingException e) {
            
            e.printStackTrace();
        } catch (JMSException e) {
            
            e.printStackTrace();
        }
        
        // ottengo i administered object







    }
}
