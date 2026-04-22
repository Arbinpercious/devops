# DevOps Project

A simple Python application with automated CI/CD pipeline.

## Project Structure

- `app.py` - Main application file
- `requirements.txt` - Python dependencies
- `.github/workflows/ci.yml` - GitHub Actions CI/CD workflow
- `.gitignore` - Git ignore rules

## CI/CD Pipeline

The GitHub Actions workflow automatically:
1. Checks out your code
2. Sets up Python environment
3. Installs dependencies
4. Runs linting checks
5. Runs tests
6. Executes the application
7. Creates a build report

Triggered on:
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop` branches

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run locally:
   ```bash
   python app.py
   ```

## Testing

```bash
pytest tests/ -v
```

## Deployment

Push your code to GitHub and the workflow will automatically run. Check the Actions tab to see pipeline results.
