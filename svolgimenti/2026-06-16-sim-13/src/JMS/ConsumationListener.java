package JMS;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.StringTokenizer;

import javax.*;
import javax.jms.*;


public class ConsumationListener implements MessageListener {

    @Override
    public void onMessage(Message message) {

        TextMessage messageText = (TextMessage) message;

        try {
            String text = messageText.getText();
            System.out.println("[ANALYZE] " + text);

            StringTokenizer tokenizer = new StringTokenizer(text, "\\|");

            float kwh = Float.valueOf(tokenizer.nextToken());


            if (kwh > 50.0){
                
                try{
                    Files.write(Paths.get("./high_consumption.txt"),
                                    Arrays.asList(text), 
                                    StandardCharsets.UTF_8,
                                    StandardOpenOption.CREATE,
                                    StandardOpenOption.APPEND);

                }catch(IOException e){
                    e.printStackTrace();
                }
            }

        } catch (JMSException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }


    }



}
