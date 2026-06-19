import javax.jms.*;

public class TelematryListener implements MessageListener {
    
    @Override
    public void onMessage(Message message) {

        TextMessage textMessage = (TextMessage) message;

        DataProcessorThread worker = new DataProcessorThread(textMessage);

        worker.start();


    }


}
