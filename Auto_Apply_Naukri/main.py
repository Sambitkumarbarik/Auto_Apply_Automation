from playwright.sync_api import sync_playwright
import logging
from utils.config import Config
from utils.cli_parser import parse_args
from utils.data_reader import DataReader
from pages.login_page import LoginPage
from pages.home_page import HomePage
from pages.jobs_page import JobsPage
from pages.job_details_page import JobDetailsPage

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('naukri_automation.log'),
        logging.StreamHandler()
    ]
)

def main():
    # Parse command line arguments
    args = parse_args()
    
    # Initialize configuration
    config = Config()
    if not config.validate_security_key():
        logging.error("Invalid security key")
        return
    
    # Get credentials
    credentials = config.get_credentials()
    
    # Load additional info
    data_reader = DataReader()
    additional_info = data_reader.get_additional_info()
    
    # Initialize success counter
    successful_applications = 0
    
    with sync_playwright() as p:
        # Launch browser (non-headless for visibility)
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        
        try:
            # Login
            login_page = LoginPage(page)
            login_page.navigate()
            if not login_page.login(credentials['email'], credentials['password']):
                logging.error("Login failed")
                return
            
            # Perform job search
            home_page = HomePage(page)
            if not home_page.search_jobs(args.role, args.location, args.experience):
                logging.error("Job search failed")
                return
            
            # Set freshness filter
            if not home_page.set_freshness_filter(args.freshness):
                logging.error("Failed to set freshness filter")
                return
            
            # Initialize page objects
            jobs_page = JobsPage(page)
            job_details_page = JobDetailsPage(page)
            
            while successful_applications < args.limit:
                # Get job listings
                jobs = jobs_page.get_job_listings()
                if not jobs:
                    logging.info("No more jobs found")
                    break
                
                # Process each job
                for job in jobs:
                    if successful_applications >= args.limit:
                        break
                        
                    logging.info(f"Processing job: {job['title']}")
                    
                    # Open job in new page
                    with context.new_page() as job_page:
                        job_details_page = JobDetailsPage(job_page)
                        
                        if not jobs_page.open_job(job['element']):
                            logging.warning(f"Failed to open job: {job['title']}")
                            continue
                        
                        # Check if we can apply directly
                        if not job_details_page.can_apply_directly():
                            logging.info(f"Skipping job {job['title']} - requires company site application")
                            continue
                        
                        # Handle additional info if needed
                        if job_details_page.needs_additional_info():
                            if not job_details_page.fill_additional_info(additional_info):
                                logging.warning(f"Failed to fill additional info for job: {job['title']}")
                                continue
                        
                        # Submit application
                        if job_details_page.submit_application():
                            successful_applications += 1
                            logging.info(f"Successfully applied to job: {job['title']}")
                        else:
                            logging.warning(f"Failed to submit application for job: {job['title']}")
                
                # Check if we should move to next page
                if successful_applications < args.limit and jobs_page.has_next_page():
                    page.click("text=Next")
                    page.wait_for_load_state("networkidle")
                else:
                    break
            
            logging.info(f"Successfully applied to {successful_applications} jobs")
            
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
        finally:
            context.close()
            browser.close()

if __name__ == "__main__":
    main()
