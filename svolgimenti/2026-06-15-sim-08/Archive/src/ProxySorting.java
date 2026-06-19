import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.net.*;

public class ProxySorting implements ISmistamento{

    private int port;

    public ProxySorting(int port){

        this.port = port;

    }

    @Override
    public void smista(String codice, double peso) {
        
        try (Socket sock = new Socket(InetAddress.getLocalHost(), this.port)){
            

            DataOutputStream to_client = new DataOutputStream(sock.getOutputStream());
            DataInputStream from_client = new DataInputStream(sock.getInputStream());

            to_client.writeUTF(codice);
            to_client.writeDouble(peso);
            
            boolean ack = from_client.readBoolean();

            if(ack){
                System.out.println("Operazione avvenuta con successo");
            }else{
                System.out.println("Operazione non riuscita");
            }


        } catch (UnknownHostException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
        
    }





}
