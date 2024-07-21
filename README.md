## Project Overview

The FinTech Toolkit is designed to streamline and enhance financial technology solutions. It includes tools for:
- **Payment Processing**: Seamlessly integrate payment gateways.
- **Investment Tracking**: Monitor and analyze investment portfolios.
- **Blockchain Analysis**: Analyze blockchain data for various applications.

## Features

- **Payment Gateway Integration**: Easy setup for various payment providers.
- **Investment Portfolio Management**: Track and manage investment assets.
- **Blockchain Analytics**: Detailed analysis of blockchain transactions and data.
- **Multilingual Support**: Available in English, Hindi, Kannada.
- **Voice Assistant**: Interact with the toolkit using voice commands.

## Technologies Used

- **Programming Languages**: Python, JavaScript
- **Libraries and Frameworks**: Flask, OpenAI, Qdrant, Deep Translator
- **APIs**: OpenAI API, Qdrant API
- **Database**: Qdrant (Vector Database)

## Installation

Command to run:
1. docker info
2. docker pull qdrant/qdrant 
3. docker run -p 6333:6333 -v .:/qdrant/storage qdrant/qdrant


############################################################
Then open the terminal in pwd:
python -m venv .venv 
cd .venv 
cd scripts 
./activate
cd ..
cd ..
pip install -r requirements.txt


4. **Set Up Environment Variables:**

    Create a `.env` file and add your API keys:

    ```env
    OPENAI_API_KEY=your_openai_api_key
  
    ```

## Usage

To run the application:

1. **Start the Flask Server:**

    ```bash
    python app.py
    ```

2. **Access the Application:**

    Open your web browser and go to `http://localhost:8000`.


## Datasets

The following datasets are used in this project:

1. [Payment Data](https://datalink.youdata.ai/muzwmt4s)
2. [Investment Data](https://www.youdata.ai/datasets/661537ce256e1f773415621e?source_link=&source_platform=&data_interests=,Payment)
3. [Blockchain Data](https://datalink.youdata.ai/m5xvvsmj)

These datasets provide the necessary information for payment processing, investment tracking, and blockchain analysis.




   
