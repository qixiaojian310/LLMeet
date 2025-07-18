# Project Deployment Guide

This project involves setting up multiple components, including the frontend, backend, model, and Livekit server. Below are the detailed deployment steps.

## 1. Setup Client

Before you begin, ensure that **Rust** and **Node.js** are installed.

- In the root directory of the project, run the following command to install **pnpm**:
  ```bash
  npm install -g pnpm
  ```

* Then, install all dependencies:

  ```bash
  pnpm install
  ```
* Finally, run the following command to start the client development environment:

  ```bash
  pnpm tauri dev
  ```

## 2. Setup Model and Backend Server

You will need a powerful computer with **GPU memory** greater than **32GB**. The server should have an independent IP address or be able to connect to another server via **SSH**.

* Install **MySQL** and run the SQL script in the `LLMeetLivekitBackend` package.

## 3. Setup Livekit Server

You need to prepare a domain name and configure DNS with your DNS provider. If you have already bound the domain to a server, you can run the following command:

```bash
curl -sSL https://get.livekit.io | bash
```

Then, create a `config.yaml` file and write the following content:

```yaml
port: 7880 # SIP port
log_level: info
rtc:
  tcp_port: 7881
  port_range_start: 50000
  port_range_end: 60000

keys:
  apiKey: # Should match the LIVEKIT_API_SECRET below
turn:
  enabled: true
  tls_port: 443
  udp_port: 3478
  domain: # TURN domain name
  cert_file: # TURN server certificate
  key_file: # TURN server private key
```

Next, install **nginx** and configure a reverse proxy to ensure everyone can connect to port **7880**. Here's an example configuration:

```nginx
server {
    listen       4431 ssl;
    server_name  example.com;

    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;

    ssl_session_cache shared:SSL:1m;
    ssl_session_timeout 5m;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    location /rtc {
        proxy_pass http://127.0.0.1:7880;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

Set the reverse proxy address and port as `VITE_LIVEKIT_WS_URL`, then run the following command to start the server:

```bash
livekit-server --config /root/livekit/config.yaml --node-ip 8.222.205.90
```

## 4. Setup Model and Backend Code

Install **miniconda** or **anaconda** on your server and download the dependencies. There are two `requirements.txt` files in the `deepseek` package and `LLMeetLivekitBackend`. You need to set up two separate environments for them. The Python version for `LLMeetLivekitBackend` is **3.11**, while `deepseek` and `whisper` use **Python 3.12**.

## 5. Setup Environment Variables

Create a `.env` file in the root directory and add the following attributes:

```env
VITE_LIVEKIT_WS_URL= # Your Livekit server domain name
VITE_BACKEND_URL= # Your backend server address
VITE_BACKEND_PORT= # Your backend server port number
```

Then create a `.env` file in the `LLMeetLivekitBackend` package and add the following attributes:

```env
MYSQL_HOST=
MYSQL_PASSWORD=
MYSQL_DATABASE=
TOKEN_SECRET_KEY= # JWT token secret key
LIVEKIT_API_KEY= apiKey
LIVEKIT_API_SECRET= # Should match the Livekit config
LIVEKIT_URL= # Your Livekit server domain name
```

## 6. Start the Services

Navigate to the `LLMeetLivekitBackend`, `deepseek`, and `whisper` packages and start the **FastAPI** services on their respective ports.

## 7. Increase Privileges

Navigate to `./src-tauri/capabilities/default.json` and add the new URL for the permission `http:default`, which is `VITE_BACKEND_URL`.
