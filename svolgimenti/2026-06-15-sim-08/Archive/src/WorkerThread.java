import java.io.*;
import java.net.*;

public class WorkerThread extends Thread{

    private Socket conn;
    private ISmistamento delegate;


    @Override
    public void run() {
        
        try {
            DataInputStream from_client = new DataInputStream(this.conn.getInputStream());
        
            DataOutputStream to_client = new DataOutputStream(this.conn.getOutputStream());

            String codice = from_client.readUTF();
            double peso = from_client.readDouble();

            System.out.println("[WORKER] invoked smistamento");
            this.delegate.smista(codice, peso);

            to_client.writeBoolean(true);

        
        } catch (IOException e) {
            e.printStackTrace();
        }finally{
            try {
                this.conn.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }

    }


    public WorkerThread(Socket sock, ISmistamento delegate){
        this.conn = sock;
        this.delegate = delegate;
    }

    


}
