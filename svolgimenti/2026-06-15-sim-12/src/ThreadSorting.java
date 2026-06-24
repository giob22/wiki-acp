import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.*;


public class ThreadSorting extends Thread {

    private String codice;
    private double peso;
    private String zona;

    public ThreadSorting(String codice, double peso, String zona) {
        this.codice = codice;
        this.peso = peso;
        this.zona = zona;
    }

    @Override
    public void run() {

        URL url;
        try {
            url = new URL("http://localhost:5000/archivia");
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();

            connection.setRequestMethod("POST");
            connection.setRequestProperty("Content-Type", "application/json; utf-8");
            connection.setRequestProperty("Accept", "application/json");

            connection.setDoOutput(true);

            String jsonInputString = String.format(
                "{\"codice\":\"%s\",\"peso\":%s,\"zona\":\"%s\"}",
                this.codice, 
                String.valueOf(this.peso), 
                this.zona
            );

            System.out.println("[SERVER] sto inviando: " + jsonInputString);

            try (OutputStream os = connection.getOutputStream()){

                byte[] input = jsonInputString.getBytes("utf-8");
                os.write(input, 0, input.length);
            }catch(Exception e){

            }

            // leggiamo la risposta FLask

            int code = connection.getResponseCode();
            System.out.println("Status Code: " + code);

            try (BufferedReader br = new BufferedReader(new InputStreamReader(connection.getInputStream(), "utf-8"))){
                StringBuilder response = new StringBuilder();
                String responseLine;
                while ((responseLine = br.readLine()) != null) {
                    response.append(responseLine.trim());
                }

                System.out.println("Risposta: " + response.toString());
            }

            
        } catch (MalformedURLException e) {
            
            e.printStackTrace();
        } catch (IOException e) {
            
            e.printStackTrace();
        }


        
    }

    



}
