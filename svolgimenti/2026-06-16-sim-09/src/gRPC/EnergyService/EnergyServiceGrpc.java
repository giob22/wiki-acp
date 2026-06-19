package gRPC.EnergyService;

import static io.grpc.MethodDescriptor.generateFullMethodName;

/**
 */
@javax.annotation.Generated(
    value = "by gRPC proto compiler (version 1.73.0)",
    comments = "Source: energyService.proto")
@io.grpc.stub.annotations.GrpcGenerated
public final class EnergyServiceGrpc {

  private EnergyServiceGrpc() {}

  public static final java.lang.String SERVICE_NAME = "energy_service.EnergyService";

  // Static method descriptors that strictly reflect the proto.
  private static volatile io.grpc.MethodDescriptor<gRPC.EnergyService.Reading,
      gRPC.EnergyService.Ack> getReportConsumptionMethod;

  @io.grpc.stub.annotations.RpcMethod(
      fullMethodName = SERVICE_NAME + '/' + "ReportConsumption",
      requestType = gRPC.EnergyService.Reading.class,
      responseType = gRPC.EnergyService.Ack.class,
      methodType = io.grpc.MethodDescriptor.MethodType.UNARY)
  public static io.grpc.MethodDescriptor<gRPC.EnergyService.Reading,
      gRPC.EnergyService.Ack> getReportConsumptionMethod() {
    io.grpc.MethodDescriptor<gRPC.EnergyService.Reading, gRPC.EnergyService.Ack> getReportConsumptionMethod;
    if ((getReportConsumptionMethod = EnergyServiceGrpc.getReportConsumptionMethod) == null) {
      synchronized (EnergyServiceGrpc.class) {
        if ((getReportConsumptionMethod = EnergyServiceGrpc.getReportConsumptionMethod) == null) {
          EnergyServiceGrpc.getReportConsumptionMethod = getReportConsumptionMethod =
              io.grpc.MethodDescriptor.<gRPC.EnergyService.Reading, gRPC.EnergyService.Ack>newBuilder()
              .setType(io.grpc.MethodDescriptor.MethodType.UNARY)
              .setFullMethodName(generateFullMethodName(SERVICE_NAME, "ReportConsumption"))
              .setSampledToLocalTracing(true)
              .setRequestMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  gRPC.EnergyService.Reading.getDefaultInstance()))
              .setResponseMarshaller(io.grpc.protobuf.ProtoUtils.marshaller(
                  gRPC.EnergyService.Ack.getDefaultInstance()))
              .setSchemaDescriptor(new EnergyServiceMethodDescriptorSupplier("ReportConsumption"))
              .build();
        }
      }
    }
    return getReportConsumptionMethod;
  }

  /**
   * Creates a new async stub that supports all call types for the service
   */
  public static EnergyServiceStub newStub(io.grpc.Channel channel) {
    io.grpc.stub.AbstractStub.StubFactory<EnergyServiceStub> factory =
      new io.grpc.stub.AbstractStub.StubFactory<EnergyServiceStub>() {
        @java.lang.Override
        public EnergyServiceStub newStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
          return new EnergyServiceStub(channel, callOptions);
        }
      };
    return EnergyServiceStub.newStub(factory, channel);
  }

  /**
   * Creates a new blocking-style stub that supports all types of calls on the service
   */
  public static EnergyServiceBlockingV2Stub newBlockingV2Stub(
      io.grpc.Channel channel) {
    io.grpc.stub.AbstractStub.StubFactory<EnergyServiceBlockingV2Stub> factory =
      new io.grpc.stub.AbstractStub.StubFactory<EnergyServiceBlockingV2Stub>() {
        @java.lang.Override
        public EnergyServiceBlockingV2Stub newStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
          return new EnergyServiceBlockingV2Stub(channel, callOptions);
        }
      };
    return EnergyServiceBlockingV2Stub.newStub(factory, channel);
  }

  /**
   * Creates a new blocking-style stub that supports unary and streaming output calls on the service
   */
  public static EnergyServiceBlockingStub newBlockingStub(
      io.grpc.Channel channel) {
    io.grpc.stub.AbstractStub.StubFactory<EnergyServiceBlockingStub> factory =
      new io.grpc.stub.AbstractStub.StubFactory<EnergyServiceBlockingStub>() {
        @java.lang.Override
        public EnergyServiceBlockingStub newStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
          return new EnergyServiceBlockingStub(channel, callOptions);
        }
      };
    return EnergyServiceBlockingStub.newStub(factory, channel);
  }

  /**
   * Creates a new ListenableFuture-style stub that supports unary calls on the service
   */
  public static EnergyServiceFutureStub newFutureStub(
      io.grpc.Channel channel) {
    io.grpc.stub.AbstractStub.StubFactory<EnergyServiceFutureStub> factory =
      new io.grpc.stub.AbstractStub.StubFactory<EnergyServiceFutureStub>() {
        @java.lang.Override
        public EnergyServiceFutureStub newStub(io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
          return new EnergyServiceFutureStub(channel, callOptions);
        }
      };
    return EnergyServiceFutureStub.newStub(factory, channel);
  }

  /**
   */
  public interface AsyncService {

    /**
     */
    default void reportConsumption(gRPC.EnergyService.Reading request,
        io.grpc.stub.StreamObserver<gRPC.EnergyService.Ack> responseObserver) {
      io.grpc.stub.ServerCalls.asyncUnimplementedUnaryCall(getReportConsumptionMethod(), responseObserver);
    }
  }

  /**
   * Base class for the server implementation of the service EnergyService.
   */
  public static abstract class EnergyServiceImplBase
      implements io.grpc.BindableService, AsyncService {

    @java.lang.Override public final io.grpc.ServerServiceDefinition bindService() {
      return EnergyServiceGrpc.bindService(this);
    }
  }

  /**
   * A stub to allow clients to do asynchronous rpc calls to service EnergyService.
   */
  public static final class EnergyServiceStub
      extends io.grpc.stub.AbstractAsyncStub<EnergyServiceStub> {
    private EnergyServiceStub(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected EnergyServiceStub build(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      return new EnergyServiceStub(channel, callOptions);
    }

    /**
     */
    public void reportConsumption(gRPC.EnergyService.Reading request,
        io.grpc.stub.StreamObserver<gRPC.EnergyService.Ack> responseObserver) {
      io.grpc.stub.ClientCalls.asyncUnaryCall(
          getChannel().newCall(getReportConsumptionMethod(), getCallOptions()), request, responseObserver);
    }
  }

  /**
   * A stub to allow clients to do synchronous rpc calls to service EnergyService.
   */
  public static final class EnergyServiceBlockingV2Stub
      extends io.grpc.stub.AbstractBlockingStub<EnergyServiceBlockingV2Stub> {
    private EnergyServiceBlockingV2Stub(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected EnergyServiceBlockingV2Stub build(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      return new EnergyServiceBlockingV2Stub(channel, callOptions);
    }

    /**
     */
    public gRPC.EnergyService.Ack reportConsumption(gRPC.EnergyService.Reading request) {
      return io.grpc.stub.ClientCalls.blockingUnaryCall(
          getChannel(), getReportConsumptionMethod(), getCallOptions(), request);
    }
  }

  /**
   * A stub to allow clients to do limited synchronous rpc calls to service EnergyService.
   */
  public static final class EnergyServiceBlockingStub
      extends io.grpc.stub.AbstractBlockingStub<EnergyServiceBlockingStub> {
    private EnergyServiceBlockingStub(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected EnergyServiceBlockingStub build(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      return new EnergyServiceBlockingStub(channel, callOptions);
    }

    /**
     */
    public gRPC.EnergyService.Ack reportConsumption(gRPC.EnergyService.Reading request) {
      return io.grpc.stub.ClientCalls.blockingUnaryCall(
          getChannel(), getReportConsumptionMethod(), getCallOptions(), request);
    }
  }

  /**
   * A stub to allow clients to do ListenableFuture-style rpc calls to service EnergyService.
   */
  public static final class EnergyServiceFutureStub
      extends io.grpc.stub.AbstractFutureStub<EnergyServiceFutureStub> {
    private EnergyServiceFutureStub(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      super(channel, callOptions);
    }

    @java.lang.Override
    protected EnergyServiceFutureStub build(
        io.grpc.Channel channel, io.grpc.CallOptions callOptions) {
      return new EnergyServiceFutureStub(channel, callOptions);
    }

    /**
     */
    public com.google.common.util.concurrent.ListenableFuture<gRPC.EnergyService.Ack> reportConsumption(
        gRPC.EnergyService.Reading request) {
      return io.grpc.stub.ClientCalls.futureUnaryCall(
          getChannel().newCall(getReportConsumptionMethod(), getCallOptions()), request);
    }
  }

  private static final int METHODID_REPORT_CONSUMPTION = 0;

  private static final class MethodHandlers<Req, Resp> implements
      io.grpc.stub.ServerCalls.UnaryMethod<Req, Resp>,
      io.grpc.stub.ServerCalls.ServerStreamingMethod<Req, Resp>,
      io.grpc.stub.ServerCalls.ClientStreamingMethod<Req, Resp>,
      io.grpc.stub.ServerCalls.BidiStreamingMethod<Req, Resp> {
    private final AsyncService serviceImpl;
    private final int methodId;

    MethodHandlers(AsyncService serviceImpl, int methodId) {
      this.serviceImpl = serviceImpl;
      this.methodId = methodId;
    }

    @java.lang.Override
    @java.lang.SuppressWarnings("unchecked")
    public void invoke(Req request, io.grpc.stub.StreamObserver<Resp> responseObserver) {
      switch (methodId) {
        case METHODID_REPORT_CONSUMPTION:
          serviceImpl.reportConsumption((gRPC.EnergyService.Reading) request,
              (io.grpc.stub.StreamObserver<gRPC.EnergyService.Ack>) responseObserver);
          break;
        default:
          throw new AssertionError();
      }
    }

    @java.lang.Override
    @java.lang.SuppressWarnings("unchecked")
    public io.grpc.stub.StreamObserver<Req> invoke(
        io.grpc.stub.StreamObserver<Resp> responseObserver) {
      switch (methodId) {
        default:
          throw new AssertionError();
      }
    }
  }

  public static final io.grpc.ServerServiceDefinition bindService(AsyncService service) {
    return io.grpc.ServerServiceDefinition.builder(getServiceDescriptor())
        .addMethod(
          getReportConsumptionMethod(),
          io.grpc.stub.ServerCalls.asyncUnaryCall(
            new MethodHandlers<
              gRPC.EnergyService.Reading,
              gRPC.EnergyService.Ack>(
                service, METHODID_REPORT_CONSUMPTION)))
        .build();
  }

  private static abstract class EnergyServiceBaseDescriptorSupplier
      implements io.grpc.protobuf.ProtoFileDescriptorSupplier, io.grpc.protobuf.ProtoServiceDescriptorSupplier {
    EnergyServiceBaseDescriptorSupplier() {}

    @java.lang.Override
    public com.google.protobuf.Descriptors.FileDescriptor getFileDescriptor() {
      return gRPC.EnergyService.EnergyServiceOuterClass.getDescriptor();
    }

    @java.lang.Override
    public com.google.protobuf.Descriptors.ServiceDescriptor getServiceDescriptor() {
      return getFileDescriptor().findServiceByName("EnergyService");
    }
  }

  private static final class EnergyServiceFileDescriptorSupplier
      extends EnergyServiceBaseDescriptorSupplier {
    EnergyServiceFileDescriptorSupplier() {}
  }

  private static final class EnergyServiceMethodDescriptorSupplier
      extends EnergyServiceBaseDescriptorSupplier
      implements io.grpc.protobuf.ProtoMethodDescriptorSupplier {
    private final java.lang.String methodName;

    EnergyServiceMethodDescriptorSupplier(java.lang.String methodName) {
      this.methodName = methodName;
    }

    @java.lang.Override
    public com.google.protobuf.Descriptors.MethodDescriptor getMethodDescriptor() {
      return getServiceDescriptor().findMethodByName(methodName);
    }
  }

  private static volatile io.grpc.ServiceDescriptor serviceDescriptor;

  public static io.grpc.ServiceDescriptor getServiceDescriptor() {
    io.grpc.ServiceDescriptor result = serviceDescriptor;
    if (result == null) {
      synchronized (EnergyServiceGrpc.class) {
        result = serviceDescriptor;
        if (result == null) {
          serviceDescriptor = result = io.grpc.ServiceDescriptor.newBuilder(SERVICE_NAME)
              .setSchemaDescriptor(new EnergyServiceFileDescriptorSupplier())
              .addMethod(getReportConsumptionMethod())
              .build();
        }
      }
    }
    return result;
  }
}
