from playwright.sync_api import Page
import logging

class HomePage:
    def __init__(self, page: Page):
        self.page = page
        self.search_input = "#qsb-keyword-sugg"
        self.location_input = "#qsb-location-sugg"
        self.experience_dropdown = "#expDroope-experienceFor"
        self.search_button = "button.qsbSubmit"

    def search_jobs(self, role: str, location: str, experience: int) -> bool:
        """
        Perform job search with given criteria
        Returns True if search successful, False otherwise
        """
        try:
            # Enter search criteria
            self.page.fill(self.search_input, role)
            self.page.fill(self.location_input, location)
            
            # Select experience
            self.page.click(self.experience_dropdown)
            self.page.click(f"text={experience} years")
            
            # Click search
            self.page.click(self.search_button)
            
            # Wait for search results
            self.page.wait_for_load_state("networkidle")
            return True
        except Exception as e:
            logging.error(f"Job search failed: {str(e)}")
            return False

    def set_freshness_filter(self, days: int) -> bool:
        """
        Set the job freshness filter
        Returns True if filter set successfully, False otherwise
        """
        try:
            freshness_map = {
                1: "Last 24 hours",
                3: "Last 3 days",
                7: "Last 7 days",
                15: "Last 15 days",
                30: "Last 30 days"
            }
            
            self.page.click("text=Date Posted")
            self.page.click(f"text={freshness_map[days]}")
            self.page.wait_for_load_state("networkidle")
            return True
        except Exception as e:
            logging.error(f"Setting freshness filter failed: {str(e)}")
            return False
