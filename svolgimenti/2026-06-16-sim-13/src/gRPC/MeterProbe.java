package gRPC;

import java.util.concurrent.ThreadLocalRandom;
import java.util.concurrent.TimeUnit;

import gRPC.EnergyService.*;
import gRPC.EnergyService.EnergyServiceGrpc.EnergyServiceBlockingStub;
import gRPC.EnergyService.Ack;
import io.grpc.*;


public class MeterProbe {

    private final EnergyServiceBlockingStub stub;

    

    public MeterProbe(ManagedChannel channel){

        this.stub = EnergyServiceGrpc.newBlockingStub(channel);
    }

    public void report(){

        for (int i = 0; i < 12; i++){
            String meter_id = "meter-" + (Math.round(Math.random() * 2) +1);

            float kwh = (ThreadLocalRandom.current().nextFloat() * 100.f);

            Reading message = Reading.newBuilder().setMeterId(meter_id).setKwg(kwh).build();


            try{
                Ack ack = this.stub.reportConsumption(message);
                System.out.println("[SENT] meter_id=" + meter_id + " kwh=" + kwh + " → status="+ ack.getStatus());
                Thread.sleep(1000);


            }catch (StatusRuntimeException | InterruptedException e){
                e.printStackTrace();
            }
        }
    }

    public static void main(String[] args){
        
        ManagedChannel channel = Grpc.newChannelBuilder("localhost:50051", InsecureChannelCredentials.create()).build();
        try{
            MeterProbe client = new MeterProbe(channel);

            client.report();
        }finally{
            try {
                channel.shutdownNow().awaitTermination(5, TimeUnit.SECONDS);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }



    }


}
