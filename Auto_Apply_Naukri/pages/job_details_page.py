from playwright.sync_api import Page
import logging

class JobDetailsPage:
    def __init__(self, page: Page):
        self.page = page
        self.apply_button = "button:has-text('Apply')"
        self.company_site_text = "text=Apply on Company Site"
        self.success_message = "text=Application Successful"

    def can_apply_directly(self) -> bool:
        """Check if job can be applied directly on Naukri"""
        return (
            self.page.is_visible(self.apply_button) and 
            not self.page.is_visible(self.company_site_text)
        )

    def needs_additional_info(self) -> bool:
        """Check if job application needs additional information"""
        try:
            # Click apply button first
            self.page.click(self.apply_button)
            # Check if any form fields appear
            return self.page.is_visible("form")
        except Exception:
            return False

    def fill_additional_info(self, info: dict) -> bool:
        """
        Fill additional information in the application form
        Returns True if form filled successfully, False otherwise
        """
        try:
            # Map form fields to info dictionary keys and fill them
            field_mappings = {
                "total_experience": "input[name='experience']",
                "current_company": "input[name='company']",
                "current_designation": "input[name='designation']",
                "current_salary": "input[name='salary']",
                "notice_period": "select[name='notice_period']",
                "resume_headline": "textarea[name='resume_headline']"
            }

            for key, selector in field_mappings.items():
                if key in info and self.page.is_visible(selector):
                    self.page.fill(selector, str(info[key]))

            return True
        except Exception as e:
            logging.error(f"Failed to fill additional info: {str(e)}")
            return False

    def submit_application(self) -> bool:
        """
        Submit the job application
        Returns True if application submitted successfully, False otherwise
        """
        try:
            submit_button = self.page.get_by_role("button", name="Submit")
            submit_button.click()
            
            # Wait for success message
            self.page.wait_for_selector(self.success_message, timeout=10000)
            return True
        except Exception as e:
            logging.error(f"Failed to submit application: {str(e)}")
            return False
