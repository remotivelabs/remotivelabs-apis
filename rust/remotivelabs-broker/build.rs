fn main() -> Result<(), Box<dyn std::error::Error>> {
    tonic_build::configure()
        .build_server(false)
        .out_dir("src/remotive_api")
        .compile(
            &[
                "common.proto",
                "functional_api.proto",
                "network_api.proto",
                "system_api.proto",
                "traffic_api.proto",
            ],
            &["../../protos"],
        )?;

    Ok(())
}
