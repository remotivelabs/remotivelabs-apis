//! Rust API RemotiveBroker with gRPC bindings.

use std::{error::Error, fs, path::Path};

use futures::{stream, Stream};
use path_slash::PathExt;
use remotive_api::base::{
    file_upload_request::Data, system_service_client::SystemServiceClient, FileDescription,
    FileUploadRequest,
};
use sha2::{Digest, Sha256};
use tonic::transport::Channel;
use walkdir::WalkDir;

use crate::remotive_api::base::{Empty, LicenseStatus};

pub mod remotive_api;

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

/// Upload file to RemotiveBroker
async fn upload_file(
    system_stub: &mut SystemServiceClient<Channel>,
    path: &str,
    dest_path: String,
) -> Result<(), Box<dyn Error>> {
    let sha256 = get_sha256(path)?;
    let chunk_size = 1000000;

    // Make the path to unix style
    let unix_destination_path = Path::new(&dest_path).to_slash().unwrap();

    let upload_iterator = generate_data(path, unix_destination_path, chunk_size, sha256).await?;
    let _response = system_stub.upload_file(upload_iterator).await?;

    Ok(())
}

/// Takes a path to a directory as argument and then walks the directory recursively
///
/// Then we filter out the folders and just keep the files
pub async fn upload_folder(
    system_stub: &mut SystemServiceClient<Channel>,
    dir: &str,
) -> Result<(), Box<dyn Error>> {
    for entry_result in WalkDir::new(dir).into_iter() {
        let entry = entry_result?;
        let path = entry.path();
        if path.is_file() {
            if let Some(path_str) = entry.path().to_str() {
                upload_file(system_stub, path_str, path_str.replace(dir, "")).await?;
            }
        }
    }

    Ok(())
}

/// Reload RemotiveBroker configuration
pub async fn reload_configuration(
    system_stub: &mut SystemServiceClient<Channel>,
) -> Result<(), Box<dyn Error>> {
    let _response = system_stub.reload_configuration(Empty {}).await?;
    Ok(())
}

/// Check RemotiveBroker license
pub async fn check_license(
    system_stub: &mut SystemServiceClient<Channel>,
) -> Result<(), Box<dyn Error>> {
    let status = system_stub
        .get_license_info(Empty {})
        .await?
        .into_inner()
        .status();

    // Don't continue if the license isn't valid
    assert!(status == LicenseStatus::Valid);
    Ok(())
}
