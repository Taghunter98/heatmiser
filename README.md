# Heatmiser Recipe Automation

## Overview

This project is a self-hosted smart heating server designed to integrate with the **Heatmiser Neo** system. It automates heating schedules (**Recipes**), monitors temperature data, and optimises energy efficiency by running during lower electricity tariff periods.

Built using **Python**, this server was originally developed to help my parents automate their **air source heat pump**, reducing energy costs while maintaining comfort. By intelligently adjusting heating schedules based on real-time conditions, it provides a **cost-effective, hands-free smart heating solution**.

## Features

- **Automated Scheduling:** Adjusts heating schedules dynamically using real-time weather data.
- **Heatmiser Neo Integration:** Seamlessly communicates with Heatmiser thermostats via API.
- **Weather API Support:** Fetches external weather data to optimise heating efficiency.
- **Database Storage:** Logs temperature data for analysis and automation.
- **Robust Logging:** Detailed logs for debugging and monitoring.

## Installation & Deployment

### Prerequisites

- Python **3.9+**
- MySQL (for database storage)
- Heatmiser Neo API access
- A valid **Weather API** key
- A virtual environment (optional but recommended)

### Setup Instructions

1. **Clone this repository:**
   ```bash
   git clone https://github.com/Taghunter98/heatmiser.git
   cd heatmiser
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Set up the database:**  
   Run the provided **database schema** on your MySQL database.

4. **Configure the `.env` file** with API keys, database credentials, and email settings:
   ```bash
   SECRET_KEY='coolSecretKey'
   HOST="192.168.4.65"
   USER="johnsmith"
   PASS="password123"
   DATABASE="Heatmiser"
   EMAIL_SENDER="coolemailprovider@gmail.com"
   EMAIL_PASSWORD="xxxxxxxxxxxxxx"
   EMAIL_RECEIVER="josh@gmail.com"
   SMTP_SERVER="smtp.gmail.com"
   SMTP_PORT=587
   ```
5. **Run the server with Gunicorn:**
   ```bash
   gunicorn -w 1 -b 0.0.0.0:6000 'app:create_app()'
   ```

### **(Optional) Setting up Docker**

If you'd like to run the application inside a Docker container instead of setting it up manually, follow these steps:

1. **Build the Docker image:**

   ```bash
   docker build -t heatmiser .
   ```

2. **Run the Docker container:**

   ```bash
   docker run -d -p 6000:6000 --name heatmiser-container heatmiser
   ```

3. **Check the logs** to verify that everything is running correctly:
   ```bash
   docker logs -f heatmiser-container
   ```

This will run the server in a Docker container, and you can easily manage it with Docker commands.

---

## Background

Managing home heating efficiently can be challenging, especially with fluctuating **energy costs** and **variable weather conditions**.

The **Heatmiser Neo** system offers built-in automation via "Recipes," allowing users to schedule heating across different rooms and times. However, manually configuring these schedules can be **time-consuming** and **cost-inefficient**—especially when energy tariffs are lower at night.

This project **enhances automation** by integrating:

- **Real-time weather data**
- **Dynamic tariff-aware adjustments**

Using the **Heatmiser API**, this system automatically **activates Recipes** based on external conditions, making home heating **smarter, more efficient, and cost-effective**.

## Heatmiser Neo Integration

This server interacts with the **Heatmiser API** to:

- Retrieve the current thermostat status.
- Adjust temperature settings dynamically.
- Automate scheduling based on real-time external factors.

## How It Works

1. The system fetches **weather forecasts** from an external API.
2. It calculates the **optimal heating schedule** based on predefined logic.
3. The server **sends API commands** to Heatmiser Neo thermostats.
4. Temperature data is **logged and analysed** for efficiency improvements.

---

## Planned Features (v1.1+)

- **Web Dashboard:** A front-end interface for monitoring and controlling schedules.
- **Clone Recipes & Profiles:** Adds missing functionality from the **Heatmiser Neo** app.

---

## Contributing

Contributions are welcome!

- **Fork the repository**
- **Open an issue**
- **Submit a pull request**

---

## License

This project is licensed under the **MIT License**.

---

_This project showcases my skills in **Python**, **API integration**, and **automation**. I'm excited to share it with the community and explore potential opportunities at **Heatmiser**!_
