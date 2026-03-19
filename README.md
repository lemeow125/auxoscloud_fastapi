# Auxos Cloud FastAPI

A simple, barebones API to quickly expose data from your Auxos inverter through a FastAPI interface.

## Features

- 🔋 **Real-time Inverter Data**: Fetch current inverter status and information
- 📊 **Analytics Data**: Access time-series energy production data
- 📈 **Inverter Reports**: Get detailed analytics reports from your Auxos inverter
- 🚀 **Docker Ready**: Pre-configured for containerized deployment

## Requirements

- Python 3.13 or higher
- [uv](https://docs.astral.sh/uv/) (for dependency management)
- Docker & Docker Compose (for containerized deployment)
- Auxos Cloud account with inverter credentials

## Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd auxoscloud_fastapi
```

### 2. Environment Setup

Create a `.env` file in the project root with your Auxos credentials:

```env
# Auxos API Configuration
AUXSOL_AUTH_USER=your-email@example.com
AUXSOL_AUTH_PASSWORD=your-password
AUXSOL_INVERTER_ID=your-inverter-id
AUXSOL_INVERTER_SN=your-inverter-serial-number

# Optional: API Configuration
AUXSOL_BASE_URL=https://eu.auxsolcloud.com/auxsol-api
AUXSOL_HOME_URL=https://www.auxsolcloud.com

# Server Configuration
BACKEND_PORT=8000
```

### 3. Running Locally

#### Using Python

```bash
# Install dependencies
uv sync

# Run the server
uv run fastapi dev --host 0.0.0.0
```

The API will be available at `http://localhost:8000`

#### Using Docker Compose

```bash
docker-compose up
```

## Troubleshooting

### Connection Issues

- Verify your Auxos credentials in the `.env` file
- Check that your inverter ID and serial number are correct
- Ensure the Auxos API is accessible from your network


