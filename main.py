# Import libraries
import socketio
import platform
from aiohttp import web
import ssl
from utils import *
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509 import Name, CertificateBuilder, load_pem_x509_certificate

VERSION = "1.0.5"

# Function to generate a self-signed SSL certificate and key
def generate_self_signed_cert():
    key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

    subject = issuer = Name([
        x509.NameAttribute(NameOID.COMMON_NAME, u'localhost')
    ])

    cert = CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.utcnow()
    ).not_valid_after(
        datetime.utcnow() + timedelta(days=365)
    ).sign(
        key, default_backend()
    )

    cert_pem = cert.public_bytes(encoding=serialization.Encoding.PEM)
    key_pem = key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    return cert_pem, key_pem

# Create a new Socket.IO server with specified port
sio = socketio.AsyncServer(cors_allowed_origins='*', logger=True)
app = web.Application()
sio.attach(app)

# Define a connection event
@sio.event
async def connect(sid, environ):
    print(f"🟢 | Client {environ['REMOTE_ADDR']} connected")
    await sio.emit("NODE_DATA", { "node": platform.node(), "version": VERSION })

# Define a message event
@sio.event
async def CAPTURE_IMAGE(sid, data):
    x = data["resolution"]["x"]
    y = data["resolution"]["y"]
    response = captureImage(x, y)
    await sio.emit("IMAGE_DATA", {"image_data": response, "node_name": platform.node()})

# Define an error event
@sio.event
def event_error(sid, error):
    print(f"Error from {sid}: {error}")

# Set the port for the Socket.IO server
if __name__ == '__main__':
    port = 8080

    # Generate self-signed SSL certificate and key
    cert_pem, key_pem = generate_self_signed_cert()

    # Create an SSL context
    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.load_cert_chain(certfile=cert_pem, keyfile=key_pem)

    # Set up the Socket.IO server over HTTPS
    sio.attach(app, ssl_context=ssl_context)

    web.run_app(app, port=port)