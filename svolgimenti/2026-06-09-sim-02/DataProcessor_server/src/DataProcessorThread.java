import java.io.FileWriter;

import javax.jms.*;


public class DataProcessorThread extends Thread {

    private TextMessage message;

    public DataProcessorThread(TextMessage message){
        this.message = message;
    }

    @Override
    public void run() {
        String text;
        try {
            text = this.message.getText();
            
            String[] data = text.split("\\|");
            
            String device_id = data[0];
            
            float value = Float.valueOf(data[1]);

            System.out.println("[RECV] device_id=" + device_id + "| value=" + value);

            if (value > 75.0){
                try (FileWriter file = new FileWriter("telemetry.txt", true)) {
                    file.write(device_id + "|" + value + "\n");
                    
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }


        } catch (JMSException e) {
            e.printStackTrace();
        }

        
    }

    

}
