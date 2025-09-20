# Naukri Auto Apply Bot

A Python-based automation tool using Playwright to automatically apply for jobs on Naukri.com using the Page Object Model (POM) pattern.

## Features

- Secure credential management with encryption
- Command-line interface for job search parameters
- Automated job application process
- Progress tracking and logging
- Handling of additional information forms
- Configurable job application limit

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Auto_Apply_Naukri
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
playwright install chromium
```

4. Configure credentials:
   - Rename `.env.example` to `.env`
   - Update the values in `.env` with your credentials
   - Set your security key in the `.env` file

## Configuration

1. Update `data/additional_info.json` with your professional details
2. Modify `.env` file with your Naukri.com credentials

## Usage

Run the script with required arguments:

```bash
python main.py --role "Python Developer" --location "Bangalore" --experience 5 --freshness 1 --limit 20
```

Arguments:
- `--role`: Job role to search for
- `--location`: Job location
- `--experience`: Years of experience
- `--freshness`: Job posting age (1, 3, 7, 15, or 30 days)
- `--limit`: Maximum number of jobs to apply (default: 20)

## Project Structure

```
naukri_automation/
├── .env                    # Environment variables
├── data/
│   └── additional_info.json # Additional application details
├── main.py                 # Main script
├── utils/
│   ├── config.py          # Configuration management
│   ├── cli_parser.py      # Command line argument parsing
│   └── data_reader.py     # JSON data reader
├── pages/
│   ├── login_page.py      # Login page actions
│   ├── home_page.py       # Home page and search actions
│   ├── jobs_page.py       # Job listings page actions
│   └── job_details_page.py # Job details and application actions
└── tests/
    └── test_naukri.py     # Test cases
```

## Testing

Run tests using pytest:

```bash
pytest tests/
```

## Logging

Logs are written to `naukri_automation.log` and also displayed in the console.

## Security

- Credentials are stored in an encrypted format
- Security key required at runtime
- Sensitive information is not logged

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License.
