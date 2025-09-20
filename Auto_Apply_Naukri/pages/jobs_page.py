from playwright.sync_api import Page
from typing import List, Dict
import logging

class JobsPage:
    def __init__(self, page: Page):
        self.page = page
        self.job_cards = ".jobTuple"
        self.job_title = ".title"

    def get_job_listings(self) -> List[Dict[str, str]]:
        """
        Get all job listings from the current page
        Returns list of jobs with their details
        """
        jobs = []
        try:
            job_elements = self.page.query_selector_all(self.job_cards)
            
            for job in job_elements:
                title = job.query_selector(self.job_title)
                if title:
                    jobs.append({
                        'title': title.inner_text(),
                        'element': job
                    })
            
            return jobs
        except Exception as e:
            logging.error(f"Failed to get job listings: {str(e)}")
            return []

    def open_job(self, job_element) -> bool:
        """
        Open a specific job listing
        Returns True if job opened successfully, False otherwise
        """
        try:
            job_element.click()
            # Wait for job details to load in new tab
            self.page.wait_for_load_state("networkidle")
            return True
        except Exception as e:
            logging.error(f"Failed to open job: {str(e)}")
            return False

    def has_next_page(self) -> bool:
        """Check if there is a next page of results"""
        return self.page.is_visible("text=Next")
