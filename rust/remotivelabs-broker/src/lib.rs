//! Rust API RemotiveBroker with gRPC bindings.

use std::{error::Error, fs, path::Path};

use futures::{stream, Stream};
use generated::base::{
    file_upload_request::Data, network_service_client::NetworkServiceClient,
    system_service_client::SystemServiceClient, traffic_service_client::TrafficServiceClient,
    FileDescription, FileUploadRequest,
};
use path_slash::PathExt;
use sha2::{Digest, Sha256};
use tonic::{
    metadata::AsciiMetadataValue,
    service::interceptor::{InterceptedService, Interceptor},
    transport::Channel,
    Request, Status,
};
use walkdir::WalkDir;

use crate::generated::base::{Empty, LicenseStatus};

pub mod generated;

#[derive(Clone)]
pub struct XApiIntercept {
    opt_x_api_key: Option<AsciiMetadataValue>,
}

impl XApiIntercept {
    fn new(x_api_key: Option<String>) -> Result<Self, Box<dyn Error>> {
        let meta_value: Option<AsciiMetadataValue> = if let Some(xapi) = x_api_key {
            Some(AsciiMetadataValue::from_str(&xapi)?)
        } else {
            None
        };

        Ok(Self {
            opt_x_api_key: meta_value,
        })
    }
}

impl Interceptor for XApiIntercept {
    fn call(&mut self, mut request: Request<()>) -> Result<Request<()>, Status> {
        if let Some(add_x_api_key) = &self.opt_x_api_key {
            request
                .metadata_mut()
                .insert("x-api-key", add_x_api_key.clone());
        }
        Ok(request)
    }
}

/// Generate the file description data in the right order that the RemotiveBroker needs
async fn generate_data(
    path: &str,
    dest_path: String,
    _chunk_size: usize,
    sha256: String,
) -> Result<impl Stream<Item = FileUploadRequest>, Box<dyn Error>> {
    // Read all the data from the file
    let buf = fs::read(path)?;

    // Create a file description with the sha256 key and file destination path
    let fd = Some(Data::FileDescription(FileDescription {
        sha256,
        path: dest_path,
    }));

    let data = Some(Data::Chunk(buf));

    // Create the upload requests with file description and data
    let file_description = FileUploadRequest { data: fd };
    let data = FileUploadRequest { data };

    Ok(stream::iter(vec![file_description, data]))
}

pub struct Connection {
    pub channel: Channel,
    pub system_stub: SystemServiceClient<InterceptedService<Channel, XApiIntercept>>,
    pub network_stub: NetworkServiceClient<InterceptedService<Channel, XApiIntercept>>,
    pub traffic_stub: TrafficServiceClient<InterceptedService<Channel, XApiIntercept>>,
}

/// Generate a sha256 key of the data in the provided file
pub fn get_sha256(path: &str) -> Result<String, Box<dyn Error>> {
    // Read all the data from the file
    let bytes = fs::read(path)?;

    // Create a hasher and add the data from the file to it
    let mut hasher = Sha256::new();
    hasher.update(bytes);

    // Generate the key and make it to a readable String
    let result = format!("{:x}", hasher.finalize());
    Ok(result)
}

impl Connection {
    pub async fn new(url: String, x_api_key: Option<String>) -> Result<Self, Box<dyn Error>> {
        let channel = Channel::from_shared(url.to_string())?.connect().await?;

        let x_api_key_intercept: XApiIntercept = XApiIntercept::new(x_api_key)?;

        Ok(Self {
            channel: channel.clone(),
            system_stub: SystemServiceClient::with_interceptor(
                channel.clone(),
                x_api_key_intercept.clone(),
            ),
            network_stub: NetworkServiceClient::with_interceptor(
                channel.clone(),
                x_api_key_intercept.clone(),
            ),
            traffic_stub: TrafficServiceClient::with_interceptor(
                channel.clone(),
                x_api_key_intercept.clone(),
            ),
        })
    }

    /// Takes a path to a directory as argument and then walks the directory recursively
    ///
    /// Then we filter out the folders and just keep the files
    pub async fn upload_folder(&mut self, dir: &str) -> Result<(), Box<dyn Error>> {
        for entry_result in WalkDir::new(dir).into_iter() {
            let entry = entry_result?;
            let path = entry.path();
            if path.is_file() {
                if let Some(path_str) = entry.path().to_str() {
                    self.upload_file(path_str, path_str.replace(dir, ""))
                        .await?;
                }
            }
        }

        Ok(())
    }

    /// Upload file to RemotiveBroker
    pub async fn upload_file(
        &mut self,
        path: &str,
        dest_path: String,
    ) -> Result<(), Box<dyn Error>> {
        let sha256 = get_sha256(path)?;
        let chunk_size = 1000000;

        // Make the path to unix style
        let unix_destination_path = Path::new(&dest_path).to_slash().unwrap();

        let upload_iterator =
            generate_data(path, unix_destination_path, chunk_size, sha256).await?;
        let _response = self.system_stub.upload_file(upload_iterator).await?;

        Ok(())
    }

    /// Reload RemotiveBroker configuration
    pub async fn reload_configuration(&mut self) -> Result<(), Box<dyn Error>> {
        let _response = self.system_stub.reload_configuration(Empty {}).await?;
        Ok(())
    }

    /// Check RemotiveBroker license
    pub async fn check_license(&mut self) -> Result<(), Box<dyn Error>> {
        let status = self
            .system_stub
            .get_license_info(Empty {})
            .await?
            .into_inner()
            .status();

        // Don't continue if the license isn't valid
        assert!(status == LicenseStatus::Valid);
        Ok(())
    }
}
