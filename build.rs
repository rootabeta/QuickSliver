// Stub to compile protobufs from Sliver for use in our client
fn main() -> Result<(), Box<dyn std::error::Error>> { 
    /* From the Sliver protobuf documentation:
     * `commonpb` - Common generic messages shared between `clientpb` and `sliverpb`. 
     *      -> Notably the generic `Request` and `Response` types, which are used as headers in gRPC request/responses.
     * `clientpb` - These messages should _only_ be sent from the client to server or vice versa.
     * `sliverpb` - These message may be sent from the client to the server or from the server to the implant and vice versa. 
     *      -> Not all messages defined in this file will appear in client<->server communication, some are specific to implant<->server.
     * `rpcpb` - gRPC service definitions
     */

    tonic_build::configure()
        .build_client(true) // We only care about the client tools
        .build_server(false)
        .compile_protos(
            &["sliver/protobuf/rpcpb/services.proto"],
            &["sliver/protobuf/"]
        )?;

    Ok(())
}
