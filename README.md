# Resume Matcher

A FastAPI-based application that matches resumes with job descriptions using AI and vector similarity search. The system stores resumes in a vector database and provides intelligent matching with interview question generation.

## Features

- **Resume Upload**: Upload resume files in .txt format
- **Vector Storage**: Efficiently store and search resumes using FAISS vector database
- **AI Matching**: Generate match scores between resumes and job descriptions
- **Interview Questions**: Automatically generate tailored interview questions
- **RESTful API**: Clean API endpoints for easy integration

## Project Structure

```
resume matcher/
├── app/
│   ├── api/
│   │   └── router.py          # API endpoints
│   ├── core/
│   │   └── config.py          # Configuration management
│   ├── models/
│   │   └── schemas.py         # Pydantic models
│   ├── services/
│   │   ├── vector_service.py  # Vector store operations
│   │   └── matching_service.py # Matching logic
│   └── utils/
│       └── file_utils.py      # File handling utilities
├── main.py                    # Application entry point
├── prompt.py                  # AI prompt templates
├── requirements.txt           # Dependencies
└── .env                       # Environment variables
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd resume-matcher
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory:
```env
OPENAI_API_KEY=your_openai_api_key_here
BASE_URL=your_openai_base_url  # Optional: for custom OpenAI endpoints
MODEL=gpt-3.5-turbo  # Or your preferred model
```

## Usage

### Starting the Application

```bash
python main.py
```

The application will start on `http://0.0.0.0:8000`

### API Endpoints

#### Upload Resume
```http
POST /upload
Content-Type: multipart/form-data

file: resume.txt (text file)
```

**Response:**
```json
{
  "message": "Resume for candidate_name added to vector store."
}
```

#### Match Resumes with Job Description
```http
POST /match
Content-Type: multipart/form-data

jdfile: job_description.txt (text file)
```

**Response:**
```json
{
  "matches": [
    {
      "candidate_name": "John Doe",
      "match_score": "85% - Strong match with required Python and ML skills",
      "interview_questions": [
        "Can you explain your experience with machine learning frameworks?",
        "How do you handle data preprocessing in your projects?",
        "Describe a challenging problem you solved using Python."
      ]
    }
  ]
}
```

### API Documentation

Once the application is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Configuration

The application uses environment variables for configuration. Key settings include:

- `OPENAI_API_KEY`: Your OpenAI API key
- `BASE_URL`: Custom OpenAI API base URL (optional)
- `MODEL`: OpenAI model to use (default: from .env)
- `VECTOR_STORE_PATH`: Path for vector store files (default: "vector_store")

## Dependencies

- **FastAPI**: Web framework for API development
- **LangChain**: Framework for LLM applications
- **FAISS**: Vector similarity search
- **HuggingFace**: Embeddings model
- **OpenAI**: Language model integration
- **Uvicorn**: ASGI server

## Development

### Adding New Features

1. **New API endpoints**: Add to `app/api/router.py`
2. **Business logic**: Add to appropriate service in `app/services/`
3. **Data models**: Add to `app/models/schemas.py`
4. **Configuration**: Update `app/core/config.py`

### Running Tests

```bash
# Add your test commands here
pytest tests/
```

## Deployment

### Local Development
```bash
python main.py
```

### Production
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Docker (Optional)
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Troubleshooting

### Common Issues

1. **Vector store not found**: Ensure you've uploaded at least one resume before matching
2. **OpenAI API errors**: Check your API key and model configuration
3. **File upload issues**: Only .txt files are supported currently

### Support

For issues and questions, please create an issue in the repository or contact the development team.