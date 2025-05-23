fn main() -> Result<(), Box<dyn std::error::Error>> {
    tonic_build::configure()
        .build_server(false)
        .out_dir("src/generated")
        .compile(
            &[
                "common.proto",
                "network_api.proto",
                "system_api.proto",
                "traffic_api.proto",
            ],
            &["../../protos"],
        )?;

    Ok(())
}
