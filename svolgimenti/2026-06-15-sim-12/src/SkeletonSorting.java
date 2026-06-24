import java.io.IOException;
import java.net.InetAddress;
import java.net.ServerSocket;
import java.net.Socket;
import java.net.UnknownHostException;

public abstract class SkeletonSorting implements ISmistamento{

    private int port;

    public SkeletonSorting(int port){
        this.port = port;
    }

    public void run_skeleton(){

        try (ServerSocket server_socket = new ServerSocket(this.port, 10, InetAddress.getLocalHost())){

            int server_port = server_socket.getLocalPort();

            System.out.println("[SERVER] listening on localhost:"+server_port);

            while(true){
                Socket conn = server_socket.accept();

                // creo il thread worker
                WorkerThread workerThread = new WorkerThread(conn, this);

                workerThread.start();
            }



        } catch (UnknownHostException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }


    }

}
