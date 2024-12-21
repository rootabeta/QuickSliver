use tonic::metadata::{MetadataValue};
use tonic::service::Interceptor;
use tonic::Request;

pub struct TokenAuthInterceptor {
    token: String,
}

impl TokenAuthInterceptor { 
    pub fn new(token: String) -> Self { 
        Self{
            token
        }
    }
}

impl Interceptor for TokenAuthInterceptor {
    fn call(&mut self, mut req: Request<()>) -> Result<Request<()>, tonic::Status> {
        // Add the token as a metadata header (Authorization in this case)
        let token_value = format!("Bearer {}", &self.token);
        unsafe { 
            let token_metadata = MetadataValue::from_shared_unchecked(token_value.into_bytes().into());
            req.metadata_mut().insert("authorization", token_metadata);
        }
        Ok(req)
    }
}
